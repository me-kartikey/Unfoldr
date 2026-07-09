import uuid
from datetime import UTC, datetime
from sqlalchemy.orm import relationship

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    original_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending"
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

    #analysis relationship with RepositoryAnalysis
    analysis = relationship(
    "RepositoryAnalysis",
    back_populates="repository",
    uselist=False
    )

    #dependencies relationship with RepositoryDependency
    dependencies = relationship(
    "RepositoryDependency",
    back_populates="repository"
    )
    
    architecture = relationship(
    "RepositoryArchitecture",
    back_populates="repository",
    uselist=False
    ) 
    from app.models.repository_dependency import RepositoryDependency
    from app.models.repository_architecture import RepositoryArchitecture