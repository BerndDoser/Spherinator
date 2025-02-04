#!/usr/bin/env python3

""" Calibrate Gaia XP continuous to spectra and store to a Parquet file.
"""

import argparse
import os
import sys
from contextlib import contextmanager
from multiprocessing import Pool

import numpy as np
import pandas as pd
import pyarrow as pa
from gaiaxpy import calibrate
from pyarrow import parquet


# Define a context manager to suppress stdout
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


list_of_arrays = [
    "bp_coefficients",
    "bp_coefficient_errors",
    "bp_coefficient_correlations",
    "rp_coefficients",
    "rp_coefficient_errors",
    "rp_coefficient_correlations",
]
sampling = np.arange(336, 1021, 2)
INPUT_FILES_SUFFIX = ".csv.gz"


def list_csv_gz_files(directory):
    return [file for file in os.listdir(directory) if file.endswith(INPUT_FILES_SUFFIX)]


def single_convert(file, path):
    data = pd.read_csv(os.path.join(path, file), comment="#", compression="gzip")

    # Convert string entries to numpy arrays
    for array in list_of_arrays:
        data[array] = data[array].apply(
            lambda x: np.fromstring(x[1:-1], dtype=np.float32, sep=",")
        )

    with suppress_stdout():
        df, _ = calibrate(data, sampling=sampling, save_file=False)

    data["flux"] = df["flux"]
    data["flux_error"] = df["flux_error"]

    # Use pyarrow to write the data to a parquet file
    table = pa.Table.from_pandas(data)

    parquet.write_table(
        table,
        f"{str(file).removesuffix(INPUT_FILES_SUFFIX)}.parquet",
        compression="snappy",
    )


def convert_to_parquet(path: str, number_of_workers: int):
    list_of_files = list_csv_gz_files(path)
    with Pool(number_of_workers) as p:
        p.starmap(single_convert, [(file, path) for file in list_of_files])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create parquet dataset with GAIA XP continuous data."
    )
    parser.add_argument(
        "path",
        help="Path to the directory containing the GAIA XP continuous data (csv files).",
    )
    parser.add_argument(
        "--number_of_workers",
        "-n",
        default=1,
        type=int,
        help="Number of workers. Default is 1.",
    )

    args = parser.parse_args()
    convert_to_parquet(args.path, args.number_of_workers)

    return 0


if __name__ == "__main__":
    sys.exit(main())
