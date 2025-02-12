import os
from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine
from fastapi import Depends
from app.config import settings


if "/data/" in settings.database_url and not os.path.exists("data"):
    os.makedirs("data")


connect_args = {"check_same_thread": False}
engine = create_engine(settings.database_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
