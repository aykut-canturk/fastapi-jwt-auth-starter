from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    __abstract__ = True
    id: int = Field(default=None, primary_key=True)
    created_user_id: int | None = Field(
        default=None, nullable=True, foreign_key="users.id"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_user_id: int | None = Field(
        default=None, nullable=True, foreign_key="users.id"
    )
    updated_at: datetime | None = Field(default=None)
    is_deleted: bool = Field(default=False)
