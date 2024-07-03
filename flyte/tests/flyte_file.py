import os

from flytekit import task, workflow
from flytekit.types.file import FlyteFile


@task
def t1() -> FlyteFile:
    p = os.path.join(os.getcwd(), "data.txt")
    f = open(p, mode="w")
    f.write("Here is some sample data.")
    f.close()
    return FlyteFile(p)


@task
def t2(ff: FlyteFile):
    ff.download()
    f = open(ff, mode="r")
    d = f.read()
    f.close()
    # do something with the data `d`


@workflow
def wf():
    ff = t1()
    t2(ff=ff)
