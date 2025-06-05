from abc import ABC, abstractmethod
from typing import Optional, Sequence
from uuid import UUID

from src.services.dto.camera import CameraDTO, CreateCameraDTO


class AbstractCameraService(ABC):
    @abstractmethod
    async def get_all_cameras(self) -> Sequence[CameraDTO]:
        ...

    @abstractmethod
    async def get_camera_by_id(self, id_camera: UUID) -> Optional[CameraDTO]:
        ...

    @abstractmethod
    async def add_camera(self, data: CreateCameraDTO) -> CameraDTO:
        ...
