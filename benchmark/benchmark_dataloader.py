import torch.utils.benchmark as benchmark
from dataset_numpy import DatasetNumpy
from dataset_rapids_parquet import DatasetRAPIDSParquet
from dataset_torch import DatasetTorch
from datasets import load_dataset
from torch.utils.data import DataLoader

from spherinator.data import ParquetDataset

label = "Benchmark DataLoader"
results = []

for dataset in [
    DatasetTorch([200, 3, 128, 128]),
    DatasetNumpy([200, 3, 128, 128]),
    DatasetRAPIDSParquet("data/Illustris_TNG_SKIRT_SDSS", "data"),
    load_dataset("parquet", data_dir="data/Illustris_TNG_SKIRT_SDSS", split="train"),
    ParquetDataset("data/Illustris_TNG_SKIRT_SDSS", "data"),
]:
    for batch_size in [32, 200]:
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
        timer = benchmark.Timer(
            stmt="for batch in dataloader: pass",
            globals={"dataloader": dataloader},
            description=dataset.__class__.__name__,
            label=label,
            sub_label=f"[{batch_size}]",
        )
        results.append(timer.blocked_autorange(min_run_time=5))

compare = benchmark.Compare(results)
compare.print()
