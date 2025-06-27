import numpy as np
from torch.utils.data import Dataset


class DatasetNumpy(Dataset):
    def __init__(self, size: list[int]):
        self.data = np.random.random(size).astype(np.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
