from fastapi import Depends
from sqlmodel import create_engine, Session
from typing import Annotated
from dotenv import load_dotenv
import os

load_dotenv()


# SQLite database file
sqlite_url = os.getenv("DB_URI")

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={"check_same_thread": False}  # required for SQLite + FastAPI
)


def get_session():
    with Session(engine) as session:
        yield session


sessionDep = Annotated[Session, Depends(get_session)]