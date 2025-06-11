from abc import ABC, abstractmethod
from typing import Optional, Sequence
from uuid import UUID


from src.infra.db.models.video import Video


class AbstractVideoRepository(ABC):

    @abstractmethod
    async def get_video_by_id(self, video_id: UUID) -> Optional[Video]:
        ...

    @abstractmethod
    async def list_by_camera(self, camera_id: UUID) -> Sequence[Video]:
        ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> Sequence[Video]:
        ...

    @abstractmethod
    async def count_by_camera(self, camera_id: UUID) -> int:
        ...

    @abstractmethod
    async def add_video(self, video: Video) -> Video:
        ...
