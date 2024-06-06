import torch
from lightning.pytorch.trainer import Trainer

from spherinator.data import ShapesDataModule
from spherinator.models import EmbeddingDecoder


def test_forward():
    model = EmbeddingDecoder()
    input = model.example_input_array
    recon = model(input)
    assert recon.shape == (1, 3, 128, 128)


def test_training(shape_path):
    model = EmbeddingDecoder(num_embeddings=4)

    datamodule = ShapesDataModule(shape_path, batch_size=2)
    datamodule.setup("fit_with_metadata")

    trainer = Trainer(
        max_epochs=1,
        enable_checkpointing=False,
        accelerator="cpu",
    )
    trainer.fit(model, datamodule=datamodule)


def test_reconstruction_loss():
    model = EmbeddingDecoder()
    image1 = torch.zeros((2, 3, 128, 128))
    image2 = torch.ones((2, 3, 128, 128))
    image3 = torch.zeros((2, 3, 128, 128))
    image3[0, 0, 0, 0] = 1.0

    assert torch.isclose(
        model.reconstruction_loss(image1, image1), torch.Tensor([0.0, 0.0]), atol=1e-3
    ).all()
    assert torch.isclose(
        model.reconstruction_loss(image1, image2), torch.Tensor([1.0, 1.0]), atol=1e-3
    ).all()
    assert torch.isclose(
        model.reconstruction_loss(image1, image3), torch.Tensor([0.009, 0.0]), atol=1e-2
    ).all()
