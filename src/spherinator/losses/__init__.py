"""
This module contains the loss functions used in Spherinator.
"""

from .combined_loss import CombinedLoss
from .perceptional_loss import PerceptualLoss
from .supervised_contrastive_loss import SupervisedContrastiveLoss

__all__ = [
    "CombinedLoss",
    "PerceptualLoss",
    "SupervisedContrastiveLoss",
]
