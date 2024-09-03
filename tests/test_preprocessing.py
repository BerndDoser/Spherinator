from preprocessing.spherinator_data_preprocessing import data_preprocess_api


def test_preprocessing(tmp_path):
    result = data_preprocess_api(
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
        output_path=tmp_path,
        debug=False,
    )
