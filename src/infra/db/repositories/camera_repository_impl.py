from uuid import UUID
from src.application.interfaces.camera_repository import AbstractCameraRepository
from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.infra.db.models.camera import Camera


class CameraRepositoryImpl(AbstractCameraRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

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

    async def add_camera(self, camera: Camera) -> Camera:
        self.session.add(camera)
        return camera
