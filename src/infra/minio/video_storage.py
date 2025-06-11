from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4
from src.infra.minio.minio_uploader import client
from minio import Minio


@dataclass
class MinioVideoStorage:
    client: Minio
    bucket_name: str = "videos"

    def __post_init__(self):
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload(self, user_id: str, file_path: Path, filename: str | None = None) -> str:
        object_name = filename or f"{user_id}/{uuid4()}{file_path.suffix}"
        self.client.fput_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            file_path=str(file_path),
        )

        return object_name


video_storage = MinioVideoStorage(client=client, bucket_name="videos")
