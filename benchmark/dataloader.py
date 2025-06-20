import torch.utils.benchmark as benchmark



import time

import torch
from torch.utils.data import DataLoader, Dataset


# Example dataset
class ExampleDataset(Dataset):
    def __init__(self, size=10000):
        self.data = torch.randn(size, 3, 224, 224)  # Simulate image data
        self.labels = torch.randint(0, 10, (size,))  # Simulate labels

    def     __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# Create dataset and dataloader
dataset = ExampleDataset()
dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

# Benchmarking the dataloader
start_time = time.time()

for epoch in range(5):  # Simulate multiple epochs
    for batch_idx, (data, labels) in enumerate(dataloader):
        # Simulate processing the batch
        pass

end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time for 5 epochs: {elapsed_time:.2f} seconds")
elapsed_time = end_time - start_time
print(f"Elapsed time for 5 epochs: {elapsed_time:.2f} seconds")




# Benchmarking function
def benchmark_dataloader(dataloader, num_epochs=5):
    timer = benchmark.Timer(
        stmt="for batch in dataloader: pass",
        globals={"dataloader": dataloader},
    )
    result = timer.timeit(num_epochs)
    print(result)

# Run benchmark
benchmark_dataloader(dataloader)benchmark_dataloader(dataloader)