import torch
from torch.utils.data import Dataset


class DatasetTorch(Dataset):
    def __init__(self, size: list[int], cache_on_gpu: bool = False):
        self.data = torch.rand(*size, dtype=torch.float32, device="cuda" if cache_on_gpu else "cpu")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
