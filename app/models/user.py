from sqlmodel import Field
from app.models.base import BaseModel


class Users(BaseModel, table=True):
    email: str = Field(nullable=False, unique=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    password: str = Field(nullable=False)
    phone_number: str = Field(nullable=True, max_length=10)
    teams_user_id: str = Field(nullable=True, max_length=40)
    push_token: str = Field(nullable=True, max_length=255)
