from datetime import datetime, time
from src.application.dto.video import VideoFilterParams
from src.application.interfaces.video_repository import AbstractVideoRepository
from uuid import UUID
from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from src.infra.db.models.user import User

from src.infra.db.models.video import TimeOfDay, TracingStatus, Video

class VideoRepositoryImpl(AbstractVideoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_video_by_id(self, video_id: UUID) -> Optional[Video]:
        return await self.session.get(Video, video_id)

    async def list_by_camera(self, camera_id: UUID) -> Sequence[Video]:
        stmt = select(Video).where(Video.camera_id == camera_id).options(selectinload(Video.author))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_by_user(self, user_id: UUID) -> Sequence[Video]:
        videos = select(Video).where(Video.author_id == user_id)
        result = await self.session.execute(videos)
        return result.scalars().all()

    async def count_by_camera(self, camera_id: UUID) -> int:
        video_count = select(func.count()).select_from(Video).where(Video.camera_id == camera_id)
        result = await self.session.execute(video_count)
        return result.scalar_one()

    async def add_video(self, video: Video) -> Video:
        self.session.add(video)
        await self.session.commit()
        return video

    async def delete_video(self, video_id: UUID) -> None:
        video = await self.get_video_by_id(video_id)
        await self.session.delete(video)
        await self.session.commit()

    async def update_video_status(self, video_id: UUID, status: TracingStatus) -> None:
        video = await self.get_video_by_id(video_id)
        if video is not None:
            video.tracing = status
            await self.session.commit()

    async def update_video_after_processing(
        self,
        video_id: UUID,
        minio_path: str,
        thumbnail_path: str,
        duration: int,
        video_resolution: str,
        fps:int,
        status: TracingStatus
    ) -> None:
        video = await self.get_video_by_id(video_id)
        if video is not None:
            video.minio_path = minio_path
            video.thumbnail_path = thumbnail_path
            video.tracing = status
            video.duration = duration
            video.video_resolution = video_resolution
            video.fps = fps
            video.counter += 1
            await self.session.commit()

    async def filter_videos(
        self,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        duration_from: Optional[int] = None,
        duration_to: Optional[int] = None,
        time_of_day: Optional[TimeOfDay] = None,
        tracing: Optional[TracingStatus] = None,
        author_name: Optional[str] = None,
    ) -> Sequence[Video]:
        query = select(Video).options(selectinload(Video.author))

        conditions = []

        if created_from:
            conditions.append(Video.created_at >= created_from)
        if created_to:
            conditions.append(Video.created_at <= created_to)

        if duration_from:
            conditions.append(Video.duration >= duration_from)
        if duration_to:
            conditions.append(Video.duration <= duration_to)

        if time_of_day:
            conditions.append(Video.time_of_day == time_of_day)

        if tracing:
            conditions.append(Video.tracing == tracing)

        if author_name:
            name_parts = author_name.lower().split()

            name_conditions = []
            for part in name_parts:
                like_pattern = f"%{part}%"
                name_conditions.append(func.lower(User.first_name).like(like_pattern))
                name_conditions.append(func.lower(User.last_name).like(like_pattern))

            author_subquery = (
                select(User.id)
                .where(or_(*name_conditions))
            )

            conditions.append(Video.author_id.in_(author_subquery))

        if conditions:
            query = query.where(and_(*conditions))
        print(str(query))
        result = await self.session.execute(query)
        videos = result.scalars().all()
        return videos
