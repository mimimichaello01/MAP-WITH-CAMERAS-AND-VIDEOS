from fastapi import Depends
from minio import Minio
from src.infra.celery.celery_app import celery_app
from src.infra.minio.minio_uploader import minio_settings
from src.infra.db.repositories.video_repository_impl import VideoRepositoryImpl
from src.infra.db.session import get_db
from src.services.video_service_impl import VideoServiceImpl


def get_minio_client() -> Minio:
    return Minio(
        endpoint=minio_settings.MINIO_ENDPOINT,
        access_key=minio_settings.MINIO_ROOT_USER,
        secret_key=minio_settings.MINIO_ROOT_PASSWORD,
        secure=False
    )


def get_video_repository(db = Depends(get_db)) -> VideoRepositoryImpl:
    return VideoRepositoryImpl(db)


def get_video_service(
    repo: VideoRepositoryImpl = Depends(get_video_repository),
) -> VideoServiceImpl:
    return VideoServiceImpl(repo, celery_app)


