import torch
from torch.utils.data import Dataset


class DatasetTorch(Dataset):
    def __init__(self, size: list[int]):
        self.data = torch.rand(*size, dtype=torch.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
