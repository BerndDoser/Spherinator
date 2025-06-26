import numpy as np
from torch.utils.data import Dataset


class DatasetNumpy(Dataset):
    def __init__(self, size: int):
        self.data = np.random.rand(size, 3, 224, 224)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
