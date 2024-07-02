import os

from flytekit import ImageSpec, task
from flytekit.types.directory import FlyteDirectory
from minio import Minio


@task(
    container_image=ImageSpec(
        packages=["minio"],
        python_version="3.10",
        registry="registry.h-its.org/doserbd/flyte",
    ),
)
def get_data() -> FlyteDirectory:

    data_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(data_dir, exist_ok=True)

    client = Minio("minio-api-itssv197.h-its.org", secure=False)

    for item in client.list_objects("illustris", recursive=True):
        client.fget_object(
            "illustris", item.object_name, os.path.join(data_dir, item.object_name)
        )

    return FlyteDirectory(path=str(data_dir))
