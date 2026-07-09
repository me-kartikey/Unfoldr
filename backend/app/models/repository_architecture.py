import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RepositoryArchitecture(Base):
    __tablename__ = "repository_architecture"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    repository_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("repositories.id"),
        nullable=False,
        unique=True
    )

    project_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    entry_points: Mapped[str] = mapped_column(
        String(2000),
        nullable=False
    )

    root_folders: Mapped[str] = mapped_column(
        String(3000),
        nullable=False
    )

    config_files: Mapped[str] = mapped_column(
        String(3000),
        nullable=False
    )

    repository = relationship(
        "Repository",
        back_populates="architecture"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )