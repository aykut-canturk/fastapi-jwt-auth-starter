import random
import string
from uuid import uuid4
from sqlmodel import Session
from fastapi import Depends
from app.services.base import BaseService
from app.utils.logger import log_info
from app.models.database import get_session
from app.models.user import Users
from app.utils.crypto import hash_password, verify_password
from app.utils.exception import ValidationError


class UserService(BaseService[Users]):
    def __init__(self, session: Session):
        super().__init__(session, Users)

    def _geneate_password(self, length=4) -> str:
        password = "".join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )
        log_info(f"Generated password: {password}")
        return password

    def _get_password_hash(self, model: Users) -> str:
        if not model.password:
            log_info(f"Generating password for {model.email}")
            model.password = self._geneate_password()
        return hash_password(model.password)

    def create(self, model: Users, commit=True):
        existing_user = self.get_by_email(model.email)
        if existing_user:
            raise ValidationError("User with this email already exists.")
        model.password = self._get_password_hash(model)
        return super().create(model, commit)

    def delete(self, model, commit=True):
        model.email = f"{model.email}-deleted-{uuid4()}"
        return super().delete(model, commit)

    def get_by_email(self, email: str) -> Users:
        return self.first(Users.email == email)

    def login(self, email: str, password: str) -> Users | None:
        user = self.get_by_email(email)
        return user if user and verify_password(password, user.password) else None


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session)
