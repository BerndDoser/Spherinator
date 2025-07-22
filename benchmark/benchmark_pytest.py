"""Pytest-based benchmarks for DataLoader performance."""

# import time

import pytest
import torch
from dataset_torch import DatasetTorch
from torch.utils.data import DataLoader


@pytest.mark.parametrize(
    "dataset",
    [
        DatasetTorch([200, 3, 128, 128]),
        # DatasetTorch([200, 3, 128, 128], cache_on_gpu=True),
        # # DatasetNumpy([200, 3, 128, 128]),
        # # ParquetDataset("data/Illustris_TNG_SKIRT_SDSS", "data"),
        # ParquetDataset(
        #     "/hits/flash/its/doserbd/SPACE/SKIRT_synthetic_images_small/parquet-v4-128-float32-snappy", "data"
        # ),
    ],
)
@pytest.mark.parametrize("batch_size", [20])
@pytest.mark.parametrize("num_workers", [1])
@pytest.mark.parametrize("pin_memory", [True])
@pytest.mark.parametrize("persistent_workers", [True])
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
        # time.sleep(0.001)
        for batch in dataloader:
            assert not batch.is_cuda
            batch = batch.to("cuda")
            torch.cuda.synchronize()  # Ensure all GPU operations are complete
            # break

    benchmark(iterate_dataloader)
    # benchmark.pedantic(iterate_dataloader, rounds=100, warmup_rounds=10, iterations=10)
