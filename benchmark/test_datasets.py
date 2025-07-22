import time

from dataset_torch import DatasetTorch
from torch.utils.data import DataLoader


start_time = time.time()
dataset = DatasetTorch([200, 3, 128, 128], cache_on_gpu=True)
# dataset = DatasetNumpy([200, 3, 128, 128])
# dataset = ParquetDataset("/hits/flash/its/doserbd/SPACE/SKIRT_synthetic_images/parquet-v4-128", "data")
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
    assert batch.is_cuda

end_time = time.time()
print(f"Time 3: {end_time - start_time:.4f} seconds")
