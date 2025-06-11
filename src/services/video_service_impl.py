from datetime import datetime
import io
from pathlib import Path
import tempfile
from typing import List, Optional
from uuid import UUID, uuid4

import aiofiles
from celery import Celery
from fastapi import HTTPException, UploadFile, status
from sqlalchemy import Sequence


from src.application.dto.video import VideoFilterParams, VideoOutDTO, VideoStatusDTO
from src.application.interfaces.video_repository import AbstractVideoRepository
from src.infra.db.converters.video_mappers import video_to_dto
from src.infra.db.converters.video_time_converter import date_to_datetime_end, date_to_datetime_start, time_to_seconds
from src.infra.db.models.video import TimeOfDay, TracingStatus, Video
from src.infra.db.repositories.video_repository_impl import VideoRepositoryImpl
from src.infra.minio.minio_uploader import client, minio_settings
from src.services.interfaces.video_service import AbstractVideoService


class VideoServiceImpl(AbstractVideoService):
    def __init__(self, video_repo: VideoRepositoryImpl, celery_app: Celery):
        self.video_repo = video_repo
        self.celery_app = celery_app

    async def _validate_video_file(self, file: UploadFile) -> None:
        if not file.filename or not file.filename.lower().endswith(".mp4"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл должен быть в формате MP4",
            )

    async def _detect_time_of_day(self) -> TimeOfDay:
        hour = datetime.now().hour

        match hour:
            case h if 6 <= h < 12:
                return TimeOfDay.MORNING
            case h if 12 <= h < 18:
                return TimeOfDay.DAY
            case h if 18 <= h < 23:
                return TimeOfDay.EVENING
            case _:
                return TimeOfDay.NIGHT

    async def upload_video(
        self, camera_id: UUID, user_id: UUID, file: UploadFile
    ) -> UUID:
        if not camera_id:
            raise HTTPException(status_code=400, detail="Не выбрана камера")

        await self._validate_video_file(file)

        video_id = uuid4()
        filename = f"{video_id}.mp4"
        local_path = Path(f"/tmp/{filename}")

        async with aiofiles.open(local_path, "wb") as out_file:
            await out_file.write(await file.read())

        video = Video(
            id=video_id,
            name=file.filename,
            duration=0,
            video_resolution="",
            fps=0,
            time_of_day=await self._detect_time_of_day(),
            tracing=TracingStatus.RUN,
            counter=0,
            author_id=user_id,
            camera_id=camera_id,
            minio_path="",
            thumbnail_path="",
        )
        await self.video_repo.add_video(video)

        self.celery_app.send_task(
            "process_video_task",
            args=[str(video_id), str(user_id), str(local_path)],
            queue="videos",
        )

        return video_id

    async def get_video_by_id(self, video_id: UUID) -> Optional[Video]:
        video = await self.video_repo.get_video_by_id(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Видео не найдено")
        return video

    async def get_status_video(self, video_id: UUID) -> VideoStatusDTO:
        video = await self.video_repo.get_video_by_id(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Видео не найдено")

        return VideoStatusDTO(video_id=UUID(str(video.id)), status=video.tracing.value)

    async def delete_video(self, video_id: UUID, user_id: UUID) -> None:
        video = await self.video_repo.get_video_by_id(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Видео не найдено")

        if video.author_id != user_id:
            raise HTTPException(
                status_code=403, detail="Недостаточно прав для удаления этого видео"
            )

        await self.video_repo.delete_video(video_id)

    async def filter_videos(self, filters: VideoFilterParams) -> List[VideoOutDTO]:
        created_from_dt = date_to_datetime_start(filters.created_from)
        created_to_dt = date_to_datetime_end(filters.created_to)
        duration_from_sec = time_to_seconds(filters.duration_from)
        duration_to_sec = time_to_seconds(filters.duration_to)

        videos = await self.video_repo.filter_videos(
            created_from=created_from_dt,
            created_to=created_to_dt,
            duration_from=duration_from_sec,
            duration_to=duration_to_sec,
            time_of_day=filters.time_of_day,
            tracing=filters.tracing,
            author_name=filters.author_name,
        )
        return [video_to_dto(video) for video in videos]

    async def get_videos_for_camera(self, camera_id: UUID) -> List[VideoOutDTO]:
        videos = await self.video_repo.list_by_camera(camera_id)
        return [video_to_dto(video) for video in videos]
