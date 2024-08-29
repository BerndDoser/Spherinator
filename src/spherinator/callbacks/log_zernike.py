import gc

import matplotlib
import numpy as np
import torch
import torchvision.transforms.functional as functional
from lightning.pytorch.callbacks import Callback
from matplotlib import figure

matplotlib.use("Agg")


class LogZernike(Callback):
    def __init__(
        self,
        num_samples: int = 6,
        indices: list[int] = [],
    ):
        super().__init__()
        self.num_samples = num_samples
        self.indices = indices

    def on_train_epoch_end(self, trainer, pl_module):
        # Return if no wandb logger is used
        if trainer.logger is None or trainer.logger.__class__.__name__ not in [
            "WandbLogger",
            "MyLogger",
        ]:
            return

        # Generate some random samples from the validation set
        data = next(iter(trainer.train_dataloader))
        samples = data[: self.num_samples].to(pl_module.device)

        # Generate reconstructions of the samples using the model
        with torch.no_grad():


            crop = functional.center_crop(samples, [pl_module.crop_size, pl_module.crop_size])
            scaled = functional.resize(
                crop, [pl_module.input_size, pl_module.input_size], antialias=True
            )

            if pl_module.__class__.__name__ == "RotationalAutoencoder":
                recon, _ = pl_module(scaled)
            else:
                out,rec = pl_module(scaled)

            #loss_recon = pl_module.criterion(out,rec)
            out = pl_module.Decoding_Function(out)
            rec = pl_module.Decoding_Function(rec)
            #print(torch.sum(out,dim=(-1,-2))[0:10])


        # Plot the original samples and their reconstructions side by side

        fig = figure.Figure(figsize=(2 * self.num_samples, 6))
        ax = fig.subplots(3, self.num_samples)
        for i in range(self.num_samples):
            ax[0, i].imshow(np.clip((scaled)[i].cpu().detach().numpy().T, 0, 1))
            ax[0, i].set_title("Original")
            ax[0, i].axis("off")
            ax[1, i].imshow(np.clip(rec[i].cpu().detach().numpy().T, 0, 1))
            ax[1, i].set_title("Reconstruction")
            ax[1, i].axis("off")
            ax[2, i].imshow(np.clip(out[i].cpu().detach().numpy().T, 0, 1))
            ax[2, i].set_title("Model_output")
            ax[2, i].axis("off")
        fig.tight_layout()

        # Log the figure at W&B
        trainer.logger.log_image(key="Reconstructions", images=[fig])

        # Clear the figure and free memory
        # Memory leak issue: https://github.com/matplotlib/matplotlib/issues/27138
        for i in range(self.num_samples):
            ax[0, i].clear()
            ax[0, i].clear()
        fig.clear()
        gc.collect()