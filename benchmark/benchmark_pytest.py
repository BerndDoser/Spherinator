"""Pytest-based benchmarks for DataLoader performance."""

import pytest
from dataset_numpy import DatasetNumpy
from dataset_torch import DatasetTorch
from torch.utils.data import DataLoader

from spherinator.data import ParquetDataset


@pytest.mark.parametrize(
    "dataset",
    [
        DatasetTorch([200, 3, 128, 128]),
        DatasetNumpy([200, 3, 128, 128]),
        ParquetDataset("data/Illustris_TNG_SKIRT_SDSS", "data"),
    ],
)
@pytest.mark.parametrize("batch_size", [32])
@pytest.mark.parametrize("num_workers", [0])
@pytest.mark.parametrize("pin_memory", [False])
@pytest.mark.parametrize("persistent_workers", [False])
def test_dataloader(benchmark, dataset, batch_size, num_workers, pin_memory, persistent_workers):
    """Benchmark DataLoader with different options."""

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=False,
        pin_memory=pin_memory,
        persistent_workers=persistent_workers,
    )

    def iterate_dataloader():
        for batch in dataloader:
            pass

    benchmark(iterate_dataloader)
    # benchmark.pedantic(iterate_dataloader, rounds=100, warmup_rounds=5, iterations=10)
