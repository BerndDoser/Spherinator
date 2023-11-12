import torch
import numpy as np

from data import ShapesDataModule


def test_fit():

    data = ShapesDataModule("tests/data/shapes", num_workers=1)
    data.setup("fit")

    assert len(data.data_train) == 4000

    dataloader = data.train_dataloader()

    assert dataloader.batch_size == 32
    assert len(dataloader) == len(data.data_train) / dataloader.batch_size
    assert dataloader.num_workers == 1

    batch = next(iter(dataloader))

    assert batch["image"].shape == (32, 3, 91, 91)
    assert batch["image"].dtype == torch.float32

    assert np.isclose(batch["image"].min(), 0.0, atol = 1e-2)
    assert np.isclose(batch["image"].max(), 1.0, atol = 1e-2)
