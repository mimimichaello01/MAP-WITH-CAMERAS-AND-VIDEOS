from uuid import UUID
from src.application.interfaces.camera_repository import AbstractCameraRepository
from typing import List, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from src.infra.db.models.camera import Camera
from src.infra.db.models.video import Video


class CameraRepositoryImpl(AbstractCameraRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def has_video(self, camera_id: UUID) -> bool:
        subquery = select(Video.id).where(Video.camera_id == camera_id).exists()
        stmt = select(subquery)
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def get_all_cameras(self) -> Sequence[Camera]:
        cameras = select(Camera)
        result = await self.session.execute(cameras)
        return result.scalars().all()

    async def get_camera_by_id(self, id_camera: UUID) -> Optional[Camera]:
        camera = select(Camera).where(Camera.id == id_camera)
        result = await self.session.execute(camera)
        return result.scalar_one_or_none()

    async def get_camera_by_camera_id(self, camera_id: str) -> Optional[Camera]:
        camera = select(Camera).where(Camera.camera_id == camera_id)
        result = await self.session.execute(camera)
        return result.scalar_one_or_none()

    async def filter_cameras(
        self,
        search: Optional[str],
        camera_type: Optional[str],
        has_video: Optional[bool],
        videos_min: Optional[int] = None,
        videos_max: Optional[int] = None,
    ) -> Sequence[Camera]:
        conditions = []
        if search:
            conditions.append(Camera.camera_name.ilike(f"%{search}%"))

        if camera_type:
            conditions.append(Camera.camera_type == camera_type)

        if has_video is not None:
            subquery = select(Video.id).where(Video.camera_id == Camera.id).exists()
            if has_video:
                conditions.append(subquery)
            else:
                conditions.append(~subquery)

        stmt = select(Camera)

        video_count = (
            select(func.count(Video.id))
            .where(Video.camera_id == Camera.id)
            .scalar_subquery()
        )

        if videos_min is not None or videos_max is not None:
            if videos_min is not None:
                conditions.append(video_count >= videos_min)
            if videos_max is not None:
                conditions.append(video_count <= videos_max)

        if conditions:
            stmt = stmt.where(*conditions)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_camera(self, camera: Camera) -> Camera:
        self.session.add(camera)
        return camera
