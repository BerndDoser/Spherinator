import os

from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory


@task
def t1() -> FlyteDirectory:
    dir = os.path.join(os.getcwd(), "results")
    os.makedirs(dir, exist_ok=True)
    with open(os.path.join(dir, "file1.txt"), "w") as file:
        file.write("Content 1\n")
    return FlyteDirectory(dir)


@task
def t2() -> FlyteDirectory:
    dir = os.path.join(os.getcwd(), "results")
    os.makedirs(dir, exist_ok=True)
    with open(os.path.join(dir, "file2.txt"), "w") as file:
        file.write("Content 2\n")
    return FlyteDirectory(dir)


@workflow
def wf() -> FlyteDirectory:
    dir1 = t1()
    dir2 = t2()
    return combine(dir1, dir2)


if __name__ == "__main__":
    print(wf())
