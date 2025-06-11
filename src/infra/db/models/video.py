from datetime import datetime, timezone
from uuid import uuid4
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Integer, String, ForeignKey, Enum as SQLEnum, func
from src.infra.db.models.camera import Camera
from src.infra.db.models.user import User
from src.infra.db.session import Base
from sqlalchemy.dialects.postgresql import UUID


class TimeOfDay(str, PyEnum):
    MORNING = "Утро"
    DAY = "День"
    EVENING = "Вечер"
    NIGHT = "Ночь"

class TracingStatus(str, PyEnum):
    PENDING = "Pending"
    DONE = "Done"
    RUN = "Run"
    ERROR = "Error"



class Video(Base):
    __tablename__ = "videos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    video_resolution: Mapped[str] = mapped_column(String, nullable=False)
    fps: Mapped[int] = mapped_column(Integer)
    time_of_day: Mapped[TimeOfDay] = mapped_column(SQLEnum(TimeOfDay), nullable=False)
    tracing: Mapped[TracingStatus] = mapped_column(SQLEnum(TracingStatus), nullable=False)
    counter: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )

    author_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    camera_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cameras.id"), nullable=False)

    author: Mapped["User"] = relationship("User", backref="videos")
    camera: Mapped["Camera"] = relationship("Camera", backref="videos")

    minio_path: Mapped[str] = mapped_column(String, nullable=False)
    thumbnail_path: Mapped[str] = mapped_column(String, nullable=False)
