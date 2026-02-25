from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, Field as PydanticField



class Employee(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100, index=True)
    email: EmailStr = Field(unique=True, index=True)
    department: str


class CreateEmployee(BaseModel):
    full_name: str = PydanticField(max_length=100)
    email: EmailStr = PydanticField(max_length=100)
    department: str
