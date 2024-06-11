import gc

import matplotlib as plt
import torch
from lightning.pytorch.callbacks import Callback

plt.use("Agg")


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

        _, metadata = trainer.train_dataloader
        indices = [int(metadata["id"])]

        # Move the samples to the device used by the model
        indices = torch.tensor(indices).to(model.device)

        # Generate reconstructions of the samples using the model
        with torch.no_grad():
            z = model.encode(indices)

        fig, ax = plt.subplots()
        ax.plot(z.cpu().numpy())

        # Log the figure at W&B
        trainer.logger.log_image(key="Latent space", images=[fig])

        # Clear the figure and free memory
        # Memory leak issue: https://github.com/matplotlib/matplotlib/issues/27138
        ax.clear()
        fig.clear()
        gc.collect()
