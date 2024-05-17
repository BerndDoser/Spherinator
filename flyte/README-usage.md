# How to use Flyte

Flyte is a platform for orchestrating machine learning and data processing workflows.
Flyte is built on top of Kubernetes.


## Quick Start

Create a new Flyte project:
```bash
flytectl create project spherinator
flytectl create project --name spherinator --id spherinator --description "test workflows"
```

Run example workflow:
```bash
pyflyte run --remote -p spherinator -d development workflow_example.py say_hello --name Ada
```

Register a workflow:
```bash
pyflyte register -p spherinator -d development workflow_parallel.py
```

Register a new version of an existing workflow:
```bash
pyflyte register -p spherinator -d development workflow_hipster.py -v 0.2
```


## Load Dictionaries from Dataclasses

> JSON does not have distinct types for integers and floating-point values.
> The presence or absence of a decimal point is not enough to distinguish between integers and non-integers.
> There is no way to distinguish between integers and floats in pure vanilla JSON
> without adding an additional schema, which in the end also means providing additional type information.

Source: https://github.com/flyteorg/flyte/issues/4505#issuecomment-1960910509

Solution: https://github.com/flyteorg/flytekit/pull/2013


## Parallelism

Flyte supports parallelism in workflows. You can define multiple tasks that can run concurrently.
Flyte will automatically manage the dependencies between tasks and ensure that they run in the correct order.
