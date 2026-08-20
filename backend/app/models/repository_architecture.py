import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
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
        index=True,
        unique=True
    )

    project_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    backend_framework: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    frontend_framework: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    architecture_pattern: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    entry_points: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    root_folders: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    config_files: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    databases: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    orms: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    authentication_methods: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    api_styles: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    devops_tools: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    cicd_tools: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    testing_frameworks: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    code_quality_tools: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    environment_files: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    deployment_platforms: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    repository_characteristics: Mapped[list] = mapped_column(
        JSONB,
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