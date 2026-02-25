from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from app.db.config import sessionDep
from app.model.employee import Employee, CreateEmployee
from app.model.attendance import Attendance
from app.api.admin.dependencies import get_current_admin

router = APIRouter(prefix="/employees", tags=["Employees"], dependencies=[Depends(get_current_admin)])

@router.post("/")
def create_employee(emp: CreateEmployee, session: sessionDep):
    # Check by email, not id (id is None on new records)
    existing = session.exec(
        select(Employee).where(Employee.email == emp.email)
    ).first()
    if existing:
        raise HTTPException(400, "Employee with this email already exists")
    emp_data = Employee(**emp.model_dump())
    session.add(emp_data)
    session.commit()
    session.refresh(emp_data)
    return emp


@router.get("/")
def list_employees(session: sessionDep):
    return session.exec(select(Employee)).all()


@router.delete("/{emp_id}")
def delete_employee(emp_id: int, session: sessionDep):
    emp = session.get(Employee, emp_id)
    if not emp:
        raise HTTPException(404, "Employee not found")

    attendance_records = session.exec(
        select(Attendance).where(Attendance.employee_id == emp_id)
    ).all()
    for record in attendance_records:
        session.delete(record)


    session.delete(emp)
    session.commit()
    return {"message": "Deleted"}