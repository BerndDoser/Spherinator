import os
from pathlib import Path

import lightning as L
from flytekit import ImageSpec, PodTemplate, Resources, task, workflow
from flytekit.types.directory import FlyteDirectory
from get_data import get_data
from kubernetes.client.models import (
    V1Container,
    V1EmptyDirVolumeSource,
    V1PodSpec,
    V1Volume,
    V1VolumeMount,
)
from tools import find_directories_with_extensions

from spherinator.data import IllustrisSdssDataModule
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
def train_model(data_dir: FlyteDirectory, max_epochs: int) -> FlyteDirectory:

    model = RotationalVariationalAutoencoderPower()

    data_dirs = find_directories_with_extensions(Path(data_dir), "fits")
    datamodule = IllustrisSdssDataModule(data_dirs)
    datamodule.setup("fit")

    model_dir = os.path.join(os.getcwd(), "model")
    trainer = L.Trainer(
        default_root_dir=model_dir,
        max_epochs=max_epochs,
        # strategy="ddp",
        # precision="16-mixed",
        # accelerator="gpu",
        inference_mode=False,
    )

    trainer.fit(model=model, datamodule=datamodule)
    return FlyteDirectory(path=str(model_dir))


@workflow
def wf(max_epochs: int) -> FlyteDirectory:
    data_dir = get_data()
    model_dir = train_model(data_dir=data_dir, max_epochs=max_epochs)
    return model_dir


if __name__ == "__main__":
    print(f"Running workflow() {wf()}")
