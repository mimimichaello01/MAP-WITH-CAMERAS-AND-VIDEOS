from src.application.dto.video import VideoOutDTO
from src.infra.db.models.video import Video


def video_to_dto(video: Video) -> VideoOutDTO:
    return VideoOutDTO(
        id=str(video.id),
        name=video.name,
        duration=video.duration,
        video_resolution=video.video_resolution,
        fps=video.fps,
        time_of_day=video.time_of_day.value,
        tracing=video.tracing.value,
        author=f"{video.author.first_name} {video.author.last_name}",
        counter=video.counter,
    )
