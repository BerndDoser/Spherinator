import time

import torch

# from dataset_torch import DatasetTorch
from torch.utils.data import DataLoader

from spherinator.data import ParquetDataset

start_time = time.time()
# dataset = DatasetTorch([200, 3, 128, 128], cache_on_gpu=True)
# dataset = DatasetNumpy([200, 3, 128, 128])
dataset = ParquetDataset("/hits/flash/its/doserbd/SPACE/SKIRT_synthetic_images/parquet-v4-128", "data")
end_time = time.time()
print(f"Time 1: {end_time - start_time:.4f} seconds")

start_time = time.time()
dataloader = DataLoader(
    dataset,
    batch_size=20,
    num_workers=0,
    shuffle=False,
    pin_memory=False,
    persistent_workers=False,
)
end_time = time.time()
print(f"Time 2: {end_time - start_time:.4f} seconds")

start_time = time.time()
for batch in dataloader:
    assert not batch.is_cuda
    batch = batch.to("cuda")
    torch.cuda.synchronize()  # Ensure all GPU operations are complete

end_time = time.time()
print(f"Time 3: {end_time - start_time:.4f} seconds")
