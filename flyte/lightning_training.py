from flytekit import ContainerTask, ImageSpec, PodTemplate, Resources, kwtypes
from flytekit.types.file import FlyteFile
from kubernetes.client.models import (
    V1Container,
    V1EmptyDirVolumeSource,
    V1PodSpec,
    V1Volume,
    V1VolumeMount,
)

custom_image = ImageSpec(
    packages=["spherinator"],
    cuda="12.1.0",
    python_version="3.12",
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


lightning_training_task = ContainerTask(
    name="lightning_training_task",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=FlyteFile),
    outputs=kwtypes(area=float, metadata=str),
    image=custom_image,
    pod_template=custom_pod_template,
    requests=Resources(mem="32Gi", cpu="48", gpu="1", ephemeral_storage="100Gi"),
    command=[
        "spherinator",
        "fit",
        "-c {{.inputs.a}}",
        "/var/outputs",
    ],
)

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--config_file", type=str)
    args = parser.parse_args()

    print(f"Running task() {(lightning_training_task(config_file=args.config_file))}")
