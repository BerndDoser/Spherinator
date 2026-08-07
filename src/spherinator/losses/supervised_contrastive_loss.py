import torch
import torch.nn as nn
import torch.nn.functional as F


class SupervisedContrastiveLoss(nn.Module):
    """Supervised contrastive loss (Khosla et al., 2020) on hyperspherical embeddings.

    Pulls embeddings sharing the same label together and pushes embeddings with
    different labels apart, using cosine similarities scaled by a temperature.

    Args:
        temperature: Scales the cosine similarities (smaller = harder separation).
    """

    def __init__(self, temperature: float = 0.1):
        if temperature <= 0:
            raise ValueError("temperature must be positive")
        super().__init__()
        self.temperature = temperature

    def forward(self, mu: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        """
        Args:
            mu: (B, D) embeddings, e.g. Power-Spherical mu-vectors on the unit sphere.
                They are re-normalized here, so unnormalized inputs are fine as well.
            labels: (B,) integer class labels.

        Returns:
            Scalar loss, averaged over all anchors that have at least one positive
            partner in the batch. Returns zero if there is no such anchor.
        """
        if mu.ndim != 2:
            raise ValueError(f"mu must be of shape (B, D), got {tuple(mu.shape)}")
        if labels.shape[0] != mu.shape[0]:
            raise ValueError("mu and labels must have the same batch size")

        device = mu.device
        batch_size = mu.shape[0]

        mu = F.normalize(mu, dim=1)

        # Cosine similarity matrix (B, B)
        sim_matrix = torch.matmul(mu, mu.T) / self.temperature

        # Mask out the diagonal, a sample is never its own positive or negative
        self_mask = torch.eye(batch_size, dtype=torch.bool, device=device)

        # Positive pairs: same label, excluding the sample itself
        labels = labels.contiguous().view(-1, 1)
        pos_mask = torch.eq(labels, labels.T) & ~self_mask

        # Denominator over all other samples (positives + negatives).
        # logsumexp subtracts the row maximum internally, so this is numerically
        # stable without an epsilon.
        log_denom = torch.logsumexp(sim_matrix.masked_fill(self_mask, float("-inf")), dim=1, keepdim=True)
        log_prob = sim_matrix - log_denom

        # Average over the positive pairs of each anchor
        num_pos = pos_mask.sum(dim=1)
        valid = num_pos > 0
        if not valid.any():
            return mu.sum() * 0.0

        mean_log_prob_pos = (pos_mask * log_prob).sum(dim=1)[valid] / num_pos[valid]

        return -mean_log_prob_pos.mean()
