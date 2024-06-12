import gc

import matplotlib.pyplot as plt
import numpy as np
import torch
from lightning.pytorch.callbacks import Callback

# plt.use("Agg")


class LatentSpaceMonitorCallback(Callback):
    def __init__(
        self,
    ):
        """
        Callback to monitor the latent space of the model during training.
        """
        super().__init__()

    def on_train_epoch_end(self, trainer, model):
        # Return if no wandb logger is used
        if trainer.logger is None or trainer.logger.__class__.__name__ not in [
            "WandbLogger",
            "MyLogger",
        ]:
            return

        z = np.empty((0, 2), float)
        # Get the latent space of the model
        for _, metadata in trainer.train_dataloader:
            indices = metadata["id"]
            indices = list(map(int, indices))
            indices = torch.tensor(indices).to(model.device)

            with torch.no_grad():
                z_batch = model.encode(indices)
                z = np.append(z, z_batch.cpu().numpy(), axis=0)

        z = z.T
        fig, ax = plt.subplots()
        ax.scatter(z[0], z[1], s=1)

        # Log the figure at W&B
        trainer.logger.log_image(key="Latent space", images=[fig])

        # Clear the figure and free memory
        # Memory leak issue: https://github.com/matplotlib/matplotlib/issues/27138
        ax.clear()
        fig.clear()
        gc.collect()
