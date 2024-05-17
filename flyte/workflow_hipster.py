import os
import urllib.request
from pathlib import Path

import flytekit
from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile


@task(cache=True, cache_version="1.0")
def download_data(urls: list[str]) -> FlyteDirectory:
    working_dir = flytekit.current_context().working_directory
    local_dir = Path(os.path.join(working_dir, "shapes"))
    local_dir.mkdir(exist_ok=True)

    # get the number of digits needed to preserve the order of files in the local directory
    zfill_len = len(str(len(urls)))
    for idx, remote_location in enumerate(urls):
        local_image = os.path.join(
            # prefix the file name with the index location of the file in the original csv_urls list
            local_dir,
            f"{str(idx).zfill(zfill_len)}_{os.path.basename(remote_location)}",
        )
        urllib.request.urlretrieve(remote_location, local_image)
    return FlyteDirectory(path=str(local_dir))


@task
def list_files(directory: FlyteDirectory) -> list[str]:
    return [str(file) for file in directory.list()]


@task
def generate_hips() -> FlyteFile:
    working_dir = Path(flytekit.current_context().working_directory)
    flytefile = working_dir / "test.txt"
    with open(flytefile, "w") as f:
        f.write("This is a test file")
    return flytefile


@task
def generate_catalog(msg: str) -> FlyteFile:
    working_dir = Path(flytekit.current_context().working_directory)
    flytefile = working_dir / "test.txt"
    with open(flytefile, "w") as f:
        f.write(msg)
    return flytefile


@workflow
def hipster_workflow(urls: list[str], msg: str) -> FlyteFile:
    """HiPster Workflow"""
    data = download_data(urls=urls)
    generate_hips()
    return generate_catalog(msg=msg)


if __name__ == "__main__":
    urls = ["https://space.h-its.org/Illustris/jpg/TNG100/099/297210.jpg"]
    print(f"Running hipster_workflow() {hipster_workflow(urls=urls, msg='elephant')}")
