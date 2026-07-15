import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RepositoryDependency(Base):
    __tablename__ = "repository_dependencies"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    repository_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("repositories.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    version: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    language: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    package_manager: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    dependency_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="production"
    )

    repository = relationship(
        "Repository",
        back_populates="dependencies"
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