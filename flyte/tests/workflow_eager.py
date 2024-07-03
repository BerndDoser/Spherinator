from flytekit import task, workflow
from flytekit.experimental import eager


# Example 1
@task
def add_one(x: int) -> int:
    return x + 1


@task
def double(x: int) -> int:
    return x * 2


@eager
async def simple_eager_workflow(x: int) -> int:
    out = await add_one(x=x)
    if out < 0:
        return -1
    return await double(x=out)
