import asyncio
from pathlib import Path
from uuid import UUID

from src.infra.celery.celery_app import celery_app

from src.infra.db.models.video import TracingStatus
from src.infra.db.repositories.video_repository_impl import VideoRepositoryImpl
from src.infra.db.session import AsyncSessionLocal
from src.infra.external_services.video_processing.thumbnail import extract_thumbnail
from src.infra.external_services.video_processing.video_processing import (
    extract_video_metadata,
)
from src.infra.minio.image_storage import image_storage
from src.infra.minio.video_storage import video_storage


async def process_video(video_id: str, user_id: str, path: str):
    video_uuid = UUID(video_id)
    video_path = Path(path)

    async with AsyncSessionLocal() as session:
        video_repo = VideoRepositoryImpl(session)

        try:
            if not video_path.exists() or not video_path.is_file():
                raise FileNotFoundError(f"Файл {video_path} не найден.")

            metadata = await extract_video_metadata(path)
            thumbnail_path = await extract_thumbnail(path)

            minio_video_path = await asyncio.to_thread(
                video_storage.upload,
                user_id=user_id,
                file_path=video_path,
            )
            minio_thumbnail_path = await asyncio.to_thread(
                image_storage.upload, user_id=user_id, image_path=Path(thumbnail_path)
            )

            video = await video_repo.get_video_by_id(video_uuid)
            if not video:
                raise ValueError("Видео не найдено")

            await video_repo.update_video_after_processing(
                video_id=video_uuid,
                minio_path=minio_video_path,
                thumbnail_path=minio_thumbnail_path,
                duration=metadata.duration,
                video_resolution=metadata.resolution,
                fps=metadata.fps,
                status=TracingStatus.DONE,
            )
        except Exception as e:
            await video_repo.update_video_status(UUID(video_id), TracingStatus.ERROR)
            raise e


@celery_app.task(bind=True, name="process_video_task", max_retries=3, default_retry_delay=10)
def process_video_task(self, video_id: str, user_id: str, video_path: str):
    loop = asyncio.get_event_loop()
    try:
        return loop.run_until_complete(process_video(video_id, user_id, video_path))
    except Exception as exc:
        async def increment_counter():
            async with AsyncSessionLocal() as session:
                video_repo = VideoRepositoryImpl(session)
                video = await video_repo.get_video_by_id(UUID(video_id))
                if video:
                    video.counter += 1
                    await session.commit()
        loop.run_until_complete(increment_counter())
        raise self.retry(exc=exc)
