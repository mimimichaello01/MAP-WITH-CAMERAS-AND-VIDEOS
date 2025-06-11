from fastapi import Depends
from minio import Minio
from src.infra.celery.celery_app import celery_app
from src.infra.db.repositories.video_repository_impl import VideoRepositoryImpl
from src.infra.db.session import get_db
from src.services.video_service_impl import VideoServiceImpl





def get_video_repository(db = Depends(get_db)) -> VideoRepositoryImpl:
    return VideoRepositoryImpl(db)


def get_video_service(
    repo: VideoRepositoryImpl = Depends(get_video_repository),
) -> VideoServiceImpl:
    return VideoServiceImpl(repo, celery_app)
