import torch
import torch.utils.benchmark as benchmark
from torch.utils.data import DataLoader, Dataset


# Example dataset
class ExampleDataset(Dataset):
    def __init__(self, size=10000):
        self.data = torch.randn(size, 3, 224, 224)  # Simulate image data
        self.labels = torch.randint(0, 10, (size,))  # Simulate labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


# Create dataset and dataloader
num_threads = 4
num_runs = 5
batch_size = 32
dataset = ExampleDataset()
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=num_threads)


# Benchmark the DataLoader
timer = benchmark.Timer(
    stmt="for batch in dataloader: pass",
    globals={"dataloader": dataloader},
    num_threads=num_threads,
)
result = timer.timeit(num_runs)
print(result)
