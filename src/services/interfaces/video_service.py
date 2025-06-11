from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import UploadFile


class AbstractVideoService(ABC):

    @abstractmethod
    async def upload_video(self, camera_id: UUID, user_id: UUID, file: UploadFile) -> UUID:
        ...
