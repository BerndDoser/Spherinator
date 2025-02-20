import torch
from datasets import load_dataset

# from torchvision import transforms

dataset = load_dataset(
    "parquet",
    data_dir="/home/doserbd/data/gaia/xp_calibrated/parquet_subset",
    streaming=True,
    # transform=transforms.Compose(
    #     [
    #         transforms.ToTensor(),
    #     ]
    # ),
)

print(dataset)

dataloader = torch.utils.data.DataLoader(
    dataset["train"],
    batch_size=128,
    shuffle=False,
    num_workers=4,
)

batch = next(iter(dataloader))
# assert batch["flux"].shape == (128, 1, 343)
assert len(batch["flux"]) == 343
