from flytekit import map_task, task, workflow


@task
def double(x: int) -> int:
    return x * 2


@task
def sum_xs(xs: list[int]) -> int:
    return sum(xs)


@workflow
def wf(xs: list[int]) -> int:
    double_xs = map_task(double)(x=xs)
    return sum_xs(xs=double_xs)
