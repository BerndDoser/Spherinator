import s3fs

from spherinator.data import ImagesDataset


def test_dataset_s3():
    s3 = s3fs.S3FileSystem(
        anon=True,
        endpoint_url="http://minio-api-itssv197.h-its.org",
    )
    dataset = ImagesDataset(s3)
    assert len(dataset) == 2
    data = dataset[0]
    assert data.shape == (3, 224, 224)
