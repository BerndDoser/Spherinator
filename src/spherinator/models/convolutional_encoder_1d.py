import torch
import torch.nn as nn


class ConvolutionalEncoder1D(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        """ConvolutionalEncoder1D initializer
        Input shape: (batch_size, 1, input_dim)
        Output shape: (batch_size, output_dim)
        """
        super().__init__()

        assert input_dim % 4 == 0, "input_dim must be divisible by 4"

        self.enc1 = nn.Sequential(
            nn.Conv1d(1, 32, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm1d(32),
            nn.ReLU(),
        )  # 32 x (input_dim / 2)
        self.enc2 = nn.Sequential(
            nn.Conv1d(32, 64, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
        )  # 64 x (input_dim / 4)
        self.enc3 = nn.Sequential(
            nn.Flatten(),
            nn.Linear(int(64 * input_dim / 4), output_dim),
        )

    def forward(self, x: torch.tensor) -> torch.tensor:
        x = self.enc1(x)
        x = self.enc2(x)
        x = self.enc3(x)
        return x
