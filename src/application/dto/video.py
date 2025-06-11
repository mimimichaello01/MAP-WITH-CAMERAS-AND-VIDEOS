from datetime import date, time
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from src.infra.db.models.video import TimeOfDay, TracingStatus


class VideoMetadataDTO(BaseModel):
    name: str
    duration: int
    resolution: str
    fps: int


class VideoStatusDTO(BaseModel):
    video_id: UUID
    status: str


class VideoFilterParams(BaseModel):
    created_from: Optional[date] = None
    created_to: Optional[date] = None
    duration_from: Optional[time] = None
    duration_to: Optional[time] = None
    time_of_day: Optional[TimeOfDay] = None
    tracing: Optional[TracingStatus] = None
    author_name: Optional[str] = None

class VideoOutDTO(BaseModel):
    id: str
    name: str
    duration: int
    video_resolution: str
    fps: int
    time_of_day: str
    tracing: str
    author: str
    counter: int
