from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.infra.db.session import Base
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
