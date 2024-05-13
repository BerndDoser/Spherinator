import pandas as pd
from flytekit import task, workflow
from flytekit.types.pickle import FlytePickle


# @task decorators define the building blocks of your pipeline
@task
def generate_hips() -> str:
    return "hips tiles generated"


# @workflows decorators define the flow of data through the tasks
@workflow
def hipster_workflow() -> FlytePickle:
    """Put all of the steps together into a single workflow."""

    generate_hips()


if __name__ == "__main__":
    # You can run this script with pre-defined arguments with `python flyte_workflow.py`
    # but we recommend running it with the `pyflyte run` CLI command, as you'll see in
    # the next step of this walkthrough.
    print(f"Running hipster_workflow() {hipster_workflow()}")
