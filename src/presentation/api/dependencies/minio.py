from fastapi import Depends
from minio import Minio
from src.infra.minio.minio_storage import MinioStorage
from src.settings.base import MinioSettings


def get_minio_settings() -> MinioSettings:
    return MinioSettings()  # type: ignore


def get_minio_client(settings: MinioSettings = Depends(get_minio_settings)) -> Minio:
    return Minio(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=False,
    )


def get_video_storage(
    client: Minio = Depends(get_minio_client),
) -> MinioStorage:
    return MinioStorage(client=client, bucket_name="videos")


def get_image_storage(
    client: Minio = Depends(get_minio_client),
) -> MinioStorage:
    return MinioStorage(client=client, bucket_name="images")
