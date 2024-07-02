from minio import Minio

client = Minio("minio-api-itssv197.h-its.org", secure=False)

for item in client.list_objects("illustris", recursive=True):
    client.fget_object("illustris", item.object_name, item.object_name)
