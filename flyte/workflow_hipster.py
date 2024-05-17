from pathlib import Path

import flytekit
from flytekit import task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.pickle import FlytePickle


@task
def generate_hips() -> FlyteFile:
    working_dir = Path(flytekit.current_context().working_directory)
    flytefile = working_dir / "test.txt"
    with open(flytefile, "w") as f:
        f.write("This is a test file")
    return flytefile


@workflow
def hipster_workflow() -> FlyteFile:
    """HiPster Workflow"""
    return generate_hips()


if __name__ == "__main__":
    print(f"Running hipster_workflow() {hipster_workflow()}")
