import os

from flytekit import ImageSpec, task
from flytekit.types.directory import FlyteDirectory

from preprocessing.spherinator_data_preprocessing import data_preprocess_api


@task(cache=True, cache_version="1.0")
def get_illustris() -> FlyteDirectory:

    data_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(data_dir, exist_ok=True)

    data_preprocess_api(
        sim="TNG50-2",
        selection_type="stellar mass",
        min_mass=5e10,
        max_mass=5.2e10,  # [Msun]
        component="stars",
        objects="centrals",
        field="Masses",
        fov="scaled",  # [kpc]
        image_depth=1.0,  #  1 particles per pixel (min. S/N=sqrt(depth))
        image_size=128,
        smoothing=0.0,  # [kpc]
        image_scale="log",
        orientation="original",
        output_path=data_dir,
        debug=False,
    )

    return FlyteDirectory(path=str(data_dir))
