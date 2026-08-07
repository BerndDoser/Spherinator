import math

import pytest
import torch
import torch.nn.functional as F

from spherinator.losses import SupervisedContrastiveLoss


def reference(mu, labels, temperature):
    """Naive loop implementation of L_out^sup (Khosla et al. 2020, Eq. 2)."""
    z = F.normalize(mu, dim=1)
    batch_size = z.shape[0]
    total, num_anchors = 0.0, 0
    for i in range(batch_size):
        positives = [j for j in range(batch_size) if j != i and labels[j] == labels[i]]
        if not positives:
            continue
        denom = sum(math.exp(float(z[i] @ z[j]) / temperature) for j in range(batch_size) if j != i)
        total -= sum(math.log(math.exp(float(z[i] @ z[p]) / temperature) / denom) for p in positives) / len(positives)
        num_anchors += 1
    return total / num_anchors if num_anchors else 0.0


class TestSupervisedContrastiveLoss:
    @pytest.mark.parametrize("temperature", [0.05, 0.1, 0.5, 1.0])
    def test_matches_reference(self, temperature):
        torch.manual_seed(0)
        mu = F.normalize(torch.randn(16, 8, dtype=torch.float64), dim=1)
        labels = torch.randint(0, 4, (16,))
        result = SupervisedContrastiveLoss(temperature=temperature)(mu, labels)
        assert result.item() == pytest.approx(reference(mu, labels, temperature))

    def test_invariant_to_input_scale(self):
        torch.manual_seed(1)
        mu = torch.randn(16, 8, dtype=torch.float64)
        labels = torch.randint(0, 4, (16,))
        loss = SupervisedContrastiveLoss()
        assert loss(mu, labels).item() == pytest.approx(loss(7.3 * mu, labels).item())

    def test_anchors_without_positives_are_skipped(self):
        torch.manual_seed(2)
        mu = F.normalize(torch.randn(5, 4, dtype=torch.float64), dim=1)
        labels = torch.tensor([0, 0, 1, 2, 3])
        result = SupervisedContrastiveLoss()(mu, labels)
        assert result.item() == pytest.approx(reference(mu, labels, 0.1))

    @pytest.mark.parametrize("labels", [torch.tensor([0, 1, 2, 3, 4]), torch.tensor([0])])
    def test_no_positive_pair_gives_zero(self, labels):
        mu = torch.randn(labels.shape[0], 4, requires_grad=True)
        result = SupervisedContrastiveLoss()(mu, labels)
        assert result.item() == 0.0
        result.backward()
        assert torch.isfinite(mu.grad).all()

    def test_gradients_are_finite(self):
        mu = torch.randn(8, 4, requires_grad=True)
        SupervisedContrastiveLoss()(mu, torch.tensor([0, 0, 1, 1, 2, 2, 3, 3])).backward()
        assert torch.isfinite(mu.grad).all()
        assert not torch.allclose(mu.grad, torch.zeros_like(mu.grad))

    def test_stable_for_small_temperature(self):
        torch.manual_seed(3)
        mu = F.normalize(torch.randn(64, 16), dim=1)
        labels = torch.randint(0, 3, (64,))
        assert torch.isfinite(SupervisedContrastiveLoss(temperature=1e-3)(mu, labels))

    def test_separated_clusters_beat_shuffled_labels(self):
        mu = torch.tensor([[1.0, 0.0], [1.0, 0.0], [-1.0, 0.0], [-1.0, 0.0]])
        loss = SupervisedContrastiveLoss(temperature=0.1)
        separated = loss(mu, torch.tensor([0, 0, 1, 1]))
        shuffled = loss(mu, torch.tensor([0, 1, 0, 1]))
        assert separated.item() == pytest.approx(0.0, abs=1e-6)
        assert separated < shuffled

    def test_invalid_arguments_raise(self):
        with pytest.raises(ValueError):
            SupervisedContrastiveLoss(temperature=0.0)
        with pytest.raises(ValueError):
            SupervisedContrastiveLoss()(torch.randn(4, 3, 2), torch.zeros(4).long())
        with pytest.raises(ValueError):
            SupervisedContrastiveLoss()(torch.randn(4, 3), torch.zeros(3).long())
