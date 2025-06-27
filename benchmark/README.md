# Benchmark Dataloader

## Download the dataset

```bash
huggingface-cli download bernddoser/Illustris_TNG_SKIRT_SDSS --repo-type dataset --local-dir ./data/Illustris_TNG_SKIRT_SDSS
```

## Run the benchmark

```bash
python benchmark.py --dataset_path ./data/Illustris_TNG_SKIRT_SDSS --batch_size 64 --num_workers 4
```
