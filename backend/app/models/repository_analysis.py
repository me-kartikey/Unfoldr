import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import(
Mapped, mapped_column,relationship
)
from app.db.base import Base

class RepositoryAnalysis(Base):
    __tablename__ = "repository_analysis"

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

    total_files: Mapped[int] = mapped_column(
        nullable=False
    )

    extensions: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    languages: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    frameworks: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    libraries: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
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
    repository = relationship(
        "Repository",
        back_populates="analysis"
    )
    


    
