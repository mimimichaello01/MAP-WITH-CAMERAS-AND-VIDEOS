import json
from typing import Optional, Sequence
from uuid import UUID

from fastapi import HTTPException, status
from src.infra.db.converters.camera_convert import cameras_to_geojson
from src.infra.db.models.camera import Camera
from src.infra.db.repositories.camera_repository_impl import CameraRepositoryImpl
from src.application.dto.camera import CameraDTO, CreateCameraDTO
from src.services.interfaces.camera_service import AbstractCameraService
from src.infra.redis.redis import redis_client


class CameraServiceImpl(AbstractCameraService):
    def __init__(self, camera_repo: CameraRepositoryImpl):
        self.camera_repo = camera_repo

    async def camera_to_dto(self, camera: Camera) -> CameraDTO:
        has_video = await self.camera_repo.has_video(camera.id)
        dto = CameraDTO.model_validate(camera)
        dto.has_video = has_video
        return dto

    async def get_all_cameras(self) -> Sequence[CameraDTO]:
        cameras = await self.camera_repo.get_all_cameras()
        dtos = [await self.camera_to_dto(camera) for camera in cameras]
        return dtos

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

        return await self.camera_to_dto(camera)

    async def filter_cameras(
        self,
        search: Optional[str],
        camera_type: Optional[str],
        has_video: Optional[bool],
        videos_min: Optional[int] = None,
        videos_max: Optional[int] = None,
    ) -> Sequence[CameraDTO]:
        cameras = await self.camera_repo.filter_cameras(
            search=search,
            camera_type=camera_type,
            has_video=has_video,
            videos_min=videos_min,
            videos_max=videos_max,
        )
        dtos = [await self.camera_to_dto(camera) for camera in cameras]
        return dtos

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
