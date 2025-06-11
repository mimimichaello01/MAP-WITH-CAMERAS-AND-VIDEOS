from datetime import date, time
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from src.application.dto.video import VideoFilterParams
from src.application.schemas.video import VideoOutSchema, VideoStatusSchema
from src.infra.db.models.user import User
from src.infra.db.models.video import TimeOfDay, TracingStatus
from src.presentation.api.dependencies.auth import get_current_user

from src.presentation.api.dependencies.video import get_video_service
from src.services.video_service_impl import VideoServiceImpl


video_router = APIRouter(prefix="/videos", tags=["Video"])


@video_router.post("/upload")
async def upload_video(
    camera_id: UUID = Form(...),
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    service: VideoServiceImpl = Depends(get_video_service),
):
    video_ids = []
    for file in files:
        video_id = await service.upload_video(camera_id, current_user.id, file)
        video_ids.append(str(video_id))
    return {"video_ids": video_ids}


@video_router.get("/{video_id}/status", response_model=VideoStatusSchema)
async def get_video_status(
    video_id: UUID,
    service: VideoServiceImpl = Depends(get_video_service),
):
    return await service.get_status_video(video_id)


@video_router.delete("/{video_id}")
async def delete_video(
    video_id: UUID,
    current_user: User = Depends(get_current_user),
    service: VideoServiceImpl = Depends(get_video_service),
):
    await service.delete_video(video_id, current_user.id)
    return {"status": "success", "message": "Видео успешно удалено."}


@video_router.get("/filter", response_model=List[VideoOutSchema])
async def filter_videos(
    created_from: Optional[date] = Query(None),
    created_to: Optional[date] = Query(None),
    duration_from: Optional[time] = Query(None),
    duration_to: Optional[time] = Query(None),
    time_of_day: Optional[TimeOfDay] = Query(None),
    tracing: Optional[TracingStatus] = Query(None),
    author_name: Optional[str] = Query(None),
    service: VideoServiceImpl = Depends(get_video_service),
):
    filters = VideoFilterParams(
        created_from=created_from,
        created_to=created_to,
        duration_from=duration_from,
        duration_to=duration_to,
        time_of_day=time_of_day,
        tracing=tracing,
        author_name=author_name,
    )
    return await service.filter_videos(filters)


@video_router.get("/{camera_id}/videos", response_model=List[VideoOutSchema])
async def get_videos_for_camera(
    camera_id: UUID,
    service: VideoServiceImpl = Depends(get_video_service),
):
    return await service.get_videos_for_camera(camera_id)
