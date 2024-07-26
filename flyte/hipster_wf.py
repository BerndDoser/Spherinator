import importlib
import os

import torch
import yaml
from flytekit import ImageSpec, PodTemplate, Resources, task, workflow
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from kubernetes.client.models import (
    V1Container,
    V1EmptyDirVolumeSource,
    V1PodSpec,
    V1Volume,
    V1VolumeMount,
)

from hipster import Hipster
from spherinator.data.spherinator_data_module import SpherinatorDataModule
from spherinator.models.spherinator_module import SpherinatorModule

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
def generate_hips(model: SpherinatorModule) -> FlyteDirectory:

    hipster_dir = os.path.join(os.getcwd(), "hipster")
    hipster = Hipster(output_folder=hipster_dir, title="Illustris")
    hipster.generate_hips(model)
    return FlyteDirectory(path=str(hipster_dir))


def generate_catalog(
    model: SpherinatorModule, datamodule: SpherinatorDataModule
) -> FlyteDirectory:

    hipster_dir = os.path.join(os.getcwd(), "hipster")
    hipster = Hipster(output_folder=hipster_dir, title="Illustris")
    hipster.generate_catalog(model, datamodule)
    return FlyteDirectory(path=str(hipster_dir))


@workflow
def wf(config_file: FlyteFile, checkpoint_file: FlyteFile) -> FlyteDirectory:

    with open(config_file, "r", encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.Loader)

    model_class_path = config["model"]["class_path"]
    module_name, class_name = model_class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    model_class = getattr(module, class_name)
    model_init_args = config["model"]["init_args"]
    model = model_class(**model_init_args)

    # Load the parameters from the checkpoint file
    device = "cuda" if torch.cuda.is_available() else "cpu"
    checkpoint = torch.load(checkpoint_file, map_location=device)
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()

    data_class_path = config["data"]["class_path"]
    module_name, class_name = data_class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    data_class = getattr(module, class_name)
    data_init_args = config["data"]["init_args"]
    datamodule = data_class(**data_init_args)

    hipster_dir = generate_hips(model=model)
    catalog_dir = generate_catalog(model=model, datamodule=datamodule)

    hipster_dir.

    return hipster_dir


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--config_file", type=str)
    parser.add_argument("--checkpoint_file", type=str)

    args = parser.parse_args()
    print(wf(config_file=args.config_file, checkpoint_file=args.checkpoint_file))
