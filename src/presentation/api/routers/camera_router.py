from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from src.application.schemas.camera import CameraSchema, CreateCameraSchema
from src.presentation.api.dependencies.camera import get_camera_service
from src.services.camera_service_impl import CameraServiceImpl
from src.application.dto.camera import CreateCameraDTO

camera_router = APIRouter(prefix="/camera", tags=["Camera"])


@camera_router.get("/cameras", response_model=list[CameraSchema])
async def filter_cameras(
    search: Optional[str] = Query(None, description="Поиск по названию камеры"),
    camera_type: Optional[str] = Query(None, description="Фильтр по типу камеры"),
    has_video: Optional[bool] = Query(None, description="Камеры с видео или без"),
    videos_min: Optional[int] = Query(None, description="Минимальное количество видео"),
    videos_max: Optional[int] = Query(
        None, description="Максимальное количество видео"
    ),
    service: CameraServiceImpl = Depends(get_camera_service),
):
    return await service.filter_cameras(
        search=search,
        camera_type=camera_type,
        has_video=has_video,
        videos_min=videos_min,
        videos_max=videos_max,
    )


@camera_router.get("/geojson")
async def list_cameras_geojson(
    service: CameraServiceImpl = Depends(get_camera_service),
):
    return await service.get_all_cameras_geojson()


@camera_router.post("/add", response_model=CameraSchema)
async def add_camera(
    data: CreateCameraSchema, service: CameraServiceImpl = Depends(get_camera_service)
):
    dto = CreateCameraDTO(**data.model_dump())
    return await service.add_camera(dto)


@camera_router.get("/{camera_id}", response_model=CameraSchema)
async def get_camera(
    camera_id: UUID, service: CameraServiceImpl = Depends(get_camera_service)
):
    return await service.get_camera_by_id(camera_id)
