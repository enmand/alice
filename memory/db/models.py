from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic.json_schema import JsonSchemaValue
from sqlalchemy import Index, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import ARRAY


class Base(DeclarativeBase):
    pass


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    group_id: Mapped[Optional[str]] = mapped_column()
    name: Mapped[Optional[str]] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    schema: Mapped[JsonSchemaValue] = mapped_column(
        JSONB,
        nullable=False,
    )
    tags: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String),
        nullable=True,
        default=[],
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        default=None,
        onupdate=datetime.now,
    )

    __table_args__ = (
        Index("idx_entities_group_id", "group_id", unique=False),
        Index(
            "idx_entities_schema_id",
            func.jsonb_extract_path(schema, "$id"),
            postgresql_using="gin",
        ),
    )
