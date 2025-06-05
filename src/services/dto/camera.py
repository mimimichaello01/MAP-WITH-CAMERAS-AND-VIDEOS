from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class CreateCameraDTO(BaseModel):
    camera_id: str
    camera_class_cd: int
    camera_class: str
    model: str
    camera_name: str
    camera_place: str
    camera_place_cd: int
    serial_number: str
    camera_type_cd: int
    camera_type: str
    camera_latitude: float
    camera_longitude: float
    archive: bool = False
    azimuth: int

class CameraDTO(CreateCameraDTO):
    id: UUID
    process_dttm: datetime
    has_video: Optional[bool] = False

    class Config:
        from_attributes = True
