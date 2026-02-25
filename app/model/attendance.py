from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import date


class Attendance(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    date: date
    status: str


class CreateAttendance(BaseModel):
    employee_id: int
    date: date
    status: str