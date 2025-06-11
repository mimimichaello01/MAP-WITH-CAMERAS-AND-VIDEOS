from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class CameraSchema(BaseModel):
    id: UUID
    camera_id: str
    camera_class_cd: int
    camera_class: str
    model: Optional[str]
    camera_name: str
    camera_place: Optional[str]
    camera_place_cd: Optional[int]
    serial_number: Optional[str]
    camera_type_cd: Optional[int]
    camera_type: Optional[str]
    camera_latitude: float
    camera_longitude: float
    archive: bool
    azimuth: Optional[int]
    process_dttm: datetime
    has_video: bool

    class Config:
        from_attributes = True


class CreateCameraSchema(BaseModel):
    camera_id: str
    camera_class_cd: int
    camera_class: str
    model: Optional[str]
    camera_name: str
    camera_place: Optional[str]
    camera_place_cd: Optional[int]
    serial_number: Optional[str]
    camera_type_cd: Optional[int]
    camera_type: Optional[str]
    camera_latitude: float
    camera_longitude: float
    archive: bool
    azimuth: Optional[int]
