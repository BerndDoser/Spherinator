import torch.utils.benchmark as benchmark
from dataset_numpy import DatasetNumpy
from dataset_rapids_parquet import DatasetRAPIDSParquet
from dataset_torch import DatasetTorch
from torch.utils.data import DataLoader

label = "Benchmark DataLoader"
results = []

for dataset in [
    DatasetTorch(10000),
    DatasetNumpy(10000),
    DatasetRAPIDSParquet("benchmark/illustris.parquet", "data"),
]:
    for batch_size in [32, 512]:
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
        timer = benchmark.Timer(
            stmt="for batch in dataloader: pass",
            globals={"dataloader": dataloader},
            description=dataset.__class__.__name__,
            label=label,
            sub_label=f"[{batch_size}]",
        )
        results.append(timer.blocked_autorange(min_run_time=1))

compare = benchmark.Compare(results)
compare.print()
