from fastapi import Depends

from src.infra.db.repositories.camera_repository_impl import CameraRepositoryImpl
from src.infra.db.session import get_db
from src.services.camera_service_impl import CameraServiceImpl


def get_camera_service(db = Depends(get_db)) -> CameraServiceImpl:
    repo = CameraRepositoryImpl(db)
    return CameraServiceImpl(repo)
