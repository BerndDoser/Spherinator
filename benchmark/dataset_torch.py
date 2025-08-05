import torch
from torch.utils.data import Dataset


class DatasetTorch(Dataset):
    def __init__(self, size: list[int], cache_on_gpu: bool = False):
        device = "cuda" if cache_on_gpu and torch.cuda.is_available() else "cpu"
        self.data = torch.rand(*size, dtype=torch.float32, device=device)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
