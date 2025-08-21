"""Model
"""
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine


SQLITE_FNAME = "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FNAME}"

connect_args = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, connect_args=connect_args)


def create_db_and_tables():
    """Create Database
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get Session
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    """Startup Hook
    """
    create_db_and_tables()
