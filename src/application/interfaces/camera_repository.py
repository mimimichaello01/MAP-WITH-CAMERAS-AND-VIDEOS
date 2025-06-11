from abc import ABC, abstractmethod
from typing import List, Optional, Sequence
from uuid import UUID

from src.infra.db.models.camera import Camera


class AbstractCameraRepository(ABC):
    @abstractmethod
    async def get_all_cameras(self) -> Sequence[Camera]: ...

    @abstractmethod
    async def get_camera_by_id(self, id_camera: UUID) -> Optional[Camera]: ...

    @abstractmethod
    async def get_camera_by_camera_id(self, camera_id: str) -> Optional[Camera]: ...

    @abstractmethod
    async def filter_cameras(
        self,
        search: Optional[str],
        camera_type: Optional[str],
        has_video: Optional[bool],
        videos_min: Optional[int] = None,
        videos_max: Optional[int] = None,
    ) -> Sequence[Camera]: ...

    @abstractmethod
    async def add_camera(self, camera: Camera) -> Camera: ...
