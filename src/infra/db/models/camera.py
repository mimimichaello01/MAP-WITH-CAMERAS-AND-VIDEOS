from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Float, Integer, String
from src.infra.db.session import Base
from sqlalchemy.dialects.postgresql import UUID


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    camera_id: Mapped[str] = mapped_column(String, comment="Номер камеры")
    camera_class_cd: Mapped[int] = mapped_column(Integer, comment="Идентификатор класса камеры")
    camera_class: Mapped[str] = mapped_column(String, comment="Класс камеры")
    model: Mapped[str] = mapped_column(String, comment="Модель")
    camera_name: Mapped[str] = mapped_column(String, comment="Название камеры")
    camera_place: Mapped[str] = mapped_column(String, comment="Адрес")
    camera_place_cd: Mapped[int] = mapped_column(Integer, comment="Идентификатор адреса")
    serial_number: Mapped[str] = mapped_column(String, comment="Серийный номер")
    camera_type_cd: Mapped[int] = mapped_column(Integer, comment="Идентификатор типа камеры")
    camera_type: Mapped[str] = mapped_column(String, comment="Тип камеры")
    camera_latitude: Mapped[float] = mapped_column(Float, comment="Широта")
    camera_longitude: Mapped[float] = mapped_column(Float, comment="Долгота")
    archive: Mapped[bool] = mapped_column(Boolean, comment="Признак архивной записи", default=False)
    azimuth: Mapped[int] = mapped_column(Integer, comment="Азимут")
    process_dttm: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), comment="Дата и время добавления записи")
    has_video: Mapped[bool] = mapped_column(default=False, comment="Наличие видео у камеры")
