from typing import Type
from pydantic import BaseModel
from app.models.user import Users
from app.schemas.base import BaseRequestSchema, BaseResponseSchema


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseRequestSchema[Users]):
    first_name: str = None
    last_name: str = None
    email: str = None
    phone_number: str = None
    teams_user_id: str = None

    @classmethod
    def model_class(cls) -> Type[Users]:
        return Users


class UserCreate(BaseRequestSchema[Users]):
    first_name: str
    last_name: str
    email: str
    phone_number: str = None
    teams_user_id: str = None

    @classmethod
    def model_class(cls) -> Type[Users]:
        return Users


class UserResponse(BaseResponseSchema[Users]):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None
    teams_user_id: str | None = None
