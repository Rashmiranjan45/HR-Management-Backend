from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from app.db.config import sessionDep
from app.model.attendance import Attendance, CreateAttendance
from app.api.admin.dependencies import get_current_admin
from app.model.employee import Employee

router = APIRouter(prefix="/attendance", tags=["Attendance"], dependencies=[Depends(get_current_admin)])

@router.post("/")
def mark_attendance(att: CreateAttendance, session: sessionDep):
    employee = session.get(Employee, att.employee_id)
    if not employee:
        raise HTTPException(404, "Employee not found")

    att_data = Attendance(**att.model_dump())
    session.add(att_data)
    session.commit()
    session.refresh(att_data)
    return att

@router.get("/employee/{emp_id}")
def get_employee_attendance(emp_id: int, session: sessionDep):
    employee = session.get(Employee, emp_id)
    if not employee:
        raise HTTPException(404, "Employee not found")
    attendance_history = session.exec(
        select(Attendance).where(Attendance.employee_id == emp_id)
    ).all()
    employee = session.exec(select(Employee).where(Employee.id == emp_id)).first()
    return {
        "employee_id": emp_id,
        "employee_name": employee.full_name,
        "attendance": [
            {"date": att.date, "status": att.status}
            for att in attendance_history
        ],
    }