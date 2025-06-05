from fastapi import APIRouter, Depends
from src.application.schemas.camera import CameraSchema, CreateCameraSchema
from src.presentation.api.dependencies.camera import get_camera_service
from src.services.camera_service_impl import CameraServiceImpl
from src.services.dto.camera import CreateCameraDTO

camera_router = APIRouter(prefix="/camera", tags=["Camera"])


@camera_router.get("/list", response_model=list[CameraSchema])
async def list_cameras(service: CameraServiceImpl = Depends(get_camera_service)):
    return await service.get_all_cameras()


@camera_router.post("/add", response_model=CameraSchema)
async def add_camera(
    data: CreateCameraSchema, service: CameraServiceImpl = Depends(get_camera_service)
):
    dto = CreateCameraDTO(**data.model_dump())
    return await service.add_camera(dto)


@camera_router.get("/geojson")
async def list_cameras_geojson(
    service: CameraServiceImpl = Depends(get_camera_service),
):
    return await service.get_all_cameras_geojson()
