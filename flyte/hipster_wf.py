import os

from flytekit import ImageSpec, PodTemplate, Resources, task, workflow
from flytekit.types.directory import FlyteDirectory
from kubernetes.client.models import (
    V1Container,
    V1EmptyDirVolumeSource,
    V1PodSpec,
    V1Volume,
    V1VolumeMount,
)

from hipster import Hipster
from spherinator.models import RotationalVariationalAutoencoderPower

custom_image = ImageSpec(
    packages=[
        "flytekitplugins-kfpytorch",
        "kubernetes",
        "spherinator",
        "minio",
    ],
    # use the cuda and python_version arguments to build a CUDA image
    cuda="12.1.0",
    python_version="3.10",
    registry="registry.h-its.org/doserbd/flyte",
)


container = V1Container(
    name=custom_image.name,
    volume_mounts=[V1VolumeMount(mount_path="/dev/shm", name="dshm")],
)
volume = V1Volume(name="dshm", empty_dir=V1EmptyDirVolumeSource(medium="Memory"))
custom_pod_template = PodTemplate(
    primary_container_name=custom_image.name,
    pod_spec=V1PodSpec(
        runtime_class_name="nvidia", containers=[container], volumes=[volume]
    ),
)


@task(
    container_image=custom_image,
    requests=Resources(mem="32Gi", cpu="48", gpu="1", ephemeral_storage="100Gi"),
    pod_template=custom_pod_template,
)
def generate_hips() -> FlyteDirectory:

    model = RotationalVariationalAutoencoderPower()

    hipster_dir = os.path.join(os.getcwd(), "hipster")
    hipster = Hipster(output_folder=hipster_dir, title="Illustris")
    hipster.generate_hips(model)
    return FlyteDirectory(path=str(hipster_dir))


@workflow
def wf() -> FlyteDirectory:
    hipster_dir = generate_hips()
    # catalog = generate_catalog()
    return hipster_dir


if __name__ == "__main__":
    print(f"Running workflow() {wf()}")
