import json
from typing import Optional, Sequence
from uuid import UUID

from fastapi import HTTPException, status
from src.infra.db.convertes.camera_convert import cameras_to_geojson
from src.infra.db.models.camera import Camera
from src.infra.db.repositories.camera_repository_impl import CameraRepositoryImpl
from src.services.dto.camera import CameraDTO, CreateCameraDTO
from src.services.interfaces.camera_service import AbstractCameraService
from src.infra.redis.redis import redis_client


class CameraServiceImpl(AbstractCameraService):
    def __init__(self, camera_repo: CameraRepositoryImpl):
        self.camera_repo = camera_repo

    async def get_all_cameras(self) -> Sequence[CameraDTO]:
        cameras = await self.camera_repo.get_all_cameras()
        return [CameraDTO.model_validate(camera) for camera in cameras]

    async def get_all_cameras_geojson(self):
        cached = await redis_client.get("geojson:cameras")
        if cached:
            return json.loads(cached)

        cameras = await self.get_all_cameras()
        geojson = cameras_to_geojson(cameras)

        await redis_client.set("geojson:cameras", json.dumps(geojson), ex=300)
        return geojson

    async def get_camera_by_id(self, id_camera: UUID) -> Optional[CameraDTO]:
        camera = await self.camera_repo.get_camera_by_id(id_camera)
        if not camera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Камера не найдена."
            )

        return CameraDTO.model_validate(camera)

    async def add_camera(self, data: CreateCameraDTO) -> CameraDTO:
        existing_camera = await self.camera_repo.get_camera_by_camera_id(data.camera_id)
        if existing_camera:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Камера с таким ID уже добавлена.",
            )

        camera = Camera(**data.model_dump())

        await self.camera_repo.add_camera(camera)
        await self.camera_repo.session.commit()
        await self.camera_repo.session.refresh(camera)

        return CameraDTO.model_validate(camera)
