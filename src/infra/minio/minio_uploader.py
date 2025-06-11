from minio import Minio

from src.settings.base import MinioSettings


minio_settings = MinioSettings() # type: ignore

client = Minio(
    endpoint=minio_settings.MINIO_ENDPOINT,
    access_key=minio_settings.MINIO_ROOT_USER,
    secret_key=minio_settings.MINIO_ROOT_PASSWORD,
    secure=False,
)
