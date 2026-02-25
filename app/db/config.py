from fastapi import Depends
from sqlmodel import create_engine,Session
from typing import Annotated
from dotenv import load_dotenv
import os

load_dotenv()

mysql_uri = os.getenv("MYSQL_URI")

engine = create_engine(mysql_uri)

def get_session():
    with Session(engine) as session:
        yield session


sessionDep = Annotated[Session, Depends(get_session)]