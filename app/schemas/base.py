from typing import Type, Generic, TypeVar
from pydantic import BaseModel as PydanticBaseModel
from app.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)

class BaseRequestSchema(PydanticBaseModel, Generic[T]):
    __abstract__ = True

    @classmethod
    def model_class(cls) -> Type[T]:
        """
        Subclasses must override this to provide the ORM model class.
        """
        raise NotImplementedError("Subclasses must define the get_model_class method.")

    def to_model(self) -> T:
        return self.model_class()(**self.dict())

class BaseResponseSchema(PydanticBaseModel, Generic[T]):
    __abstract__ = True

    @classmethod
    def from_model(cls, model: T) -> "BaseResponseSchema":
        return cls(**model.dict())
