from typing import Type, Generic, TypeVar
from datetime import datetime, UTC
from sqlmodel import Session, select, func
from app.models.base import BaseModel
from app.security import get_current_user_id

T = TypeVar("T", bound=BaseModel)


class BaseService(Generic[T]):
    __abstract__ = True
    model_class: Type[T]

    def __init__(self, session: Session, model_class: Type[T]):
        self.session = session
        self.model_class = model_class

    def query(self):
        return select(self.model_class).where(self.model_class.is_deleted.is_(False))

    def where(self, *whereclause):
        return self.query().where(*whereclause)

    def first(self, *whereclause):
        query = self.where(*whereclause)
        return self.session.exec(query).first()

    def fetch(self, *whereclause, skip: int = 0, limit: int = 10):
        query = self.where(*whereclause).offset(skip).limit(limit)
        return self.session.exec(query).all()

    def count(self, *whereclause) -> int:
        query = select(func.count(self.model_class.id)).where(*whereclause)
        return self.session.exec(query).one()

    def get(self, model_id: int) -> T | None:
        query = self.query().where(self.model_class.id == model_id)
        return self.session.exec(query).first()

    def create(self, model: T, commit: bool = True) -> T:
        model.created_user_id = get_current_user_id()
        model.created_at = datetime.now(UTC)
        model.updated_user_id = None
        model.updated_at = None

        self.session.add(model)
        if commit:
            self.session.commit()
            self.session.refresh(model)
        return model

    def update(self, model: T, commit: bool = True) -> T:
        model.updated_user_id = get_current_user_id()
        model.updated_at = datetime.now(UTC)
        self.session.add(model)
        if commit:
            self.session.commit()
            self.session.refresh(model)
        return model

    def delete(self, model: T, commit: bool = True) -> None:
        model.is_deleted = True
        self.update(model, commit)

    def delete_by_id(self, model_id: int, commit: bool = True) -> None:
        model = self.get(model_id)
        if not model:
            raise ValueError(f"{self.model_class.__name__} not found. ID: {model_id}")
        self.delete(model, commit)
