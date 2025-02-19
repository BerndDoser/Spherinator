import torch
from datasets import load_dataset

dataset = load_dataset(
    "parquet", data_dir="/home/doserbd/data/gaia/xp_calibrated/parquet_subset"
)

print(dataset)

dataloader = torch.utils.data.DataLoader(
    dataset["train"], batch_size=128, shuffle=True, num_workers=4
)


batch = next(iter(dataloader))
print(batch["flux"])
