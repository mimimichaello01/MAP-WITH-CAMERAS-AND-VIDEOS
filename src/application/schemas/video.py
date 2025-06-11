from datetime import date, time
from typing import Optional
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel

from src.application.dto.video import VideoMetadataDTO
from src.infra.db.models.video import TimeOfDay, TracingStatus


class VideoUploadSchema(BaseModel):
    video_url: str
    thumbnail_url: str
    metadata: VideoMetadataDTO


class VideoStatusSchema(BaseModel):
    video_id: UUID
    status: str

    class Config:
        from_attributes = True


class VideoFilterParams(BaseModel):
    created_from: Optional[date] = Query(None, description="Дата загрузки с")
    created_to: Optional[date] = Query(None, description="Дата загрузки до")
    duration_from: Optional[time] = Query(None, description="Продолжительность с (чч:мм:сс)")
    duration_to: Optional[time] = Query(None, description="Продолжительность до (чч:мм:сс)")
    time_of_day: Optional[TimeOfDay] = Query(None)
    tracing: Optional[TracingStatus] = Query(None)
    author_name: Optional[str] = Query(None, description="Имя или фамилия автора")


class VideoOutSchema(BaseModel):
    id: str
    name: str
    duration: int
    video_resolution: str
    fps: int
    time_of_day: str
    tracing: str
    author: str
    counter: int
