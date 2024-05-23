import math
import json
from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy import text as sqltext
from sqlalchemy.orm import Session

from mysql_database import engine, SessionLocal
from models import Base, Employees, Departments, Jobs


app = FastAPI()

Base.metadata.create_all(bind=engine)


# Pydantic model for input data validation
class EmployeesBase(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int


class DepartmentsBase(BaseModel):
    id: int
    department: str


class JobsBase(BaseModel):
    id: int
    job: str


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# API endpoint to create a new employee
@app.post("/employee/", status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeesBase, db: db_dependency):
    new_employee = Employees(**employee.dict())
    db.add(new_employee)
    db.commit()
    return new_employee


@app.get("/employee/{employee_id}", status_code=status.HTTP_200_OK)
async def get_employee(employee_id: int, db: db_dependency):
    employee = db.query(Employees).filter(Employees.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee not found. Id: {employee_id}")
    return employee


@app.delete("/employee/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(employee_id: int, db: db_dependency):
    employee = db.query(Employees).filter(Employees.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee not found. Id: {employee_id}")
    try:
        db.delete(employee)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Problem deleting employee id {employee_id}: {e}")


# API endpoint to create a new department
@app.post("/department/", status_code=status.HTTP_201_CREATED)
async def create_department(department: DepartmentsBase, db: db_dependency):
    new_department = Departments(**department.dict())
    db.add(new_department)
    db.commit()
    return new_department


@app.get("/department/{department_id}", status_code=status.HTTP_200_OK)
async def get_department(department_id: int, db: db_dependency):
    department = db.query(Departments).filter(Departments.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail=f"Department not found. Id: {department_id}")
    return department


@app.delete("/department/{department_id}", status_code=status.HTTP_200_OK)
async def delete_department(department_id: int, db: db_dependency):
    department = db.query(Departments).filter(Departments.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail=f"Department not found. Id: {department_id}")
    try:
        db.delete(department)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Problem deleting department id {department_id}: {e}")


# API endpoint to create a new department
@app.post("/job/", status_code=status.HTTP_201_CREATED)
async def create_job(job: JobsBase, db: db_dependency):
    new_job = Jobs(**job.dict())
    db.add(new_job)
    db.commit()
    return new_job


@app.get("/job/{job_id}", status_code=status.HTTP_200_OK)
async def get_job(job_id: int, db: db_dependency):
    job = db.query(Jobs).filter(Jobs.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job not found. Id: {job_id}")
    return job


@app.delete("/job/{job_id}", status_code=status.HTTP_200_OK)
async def delete_job(job_id: int, db: db_dependency):
    job = db.query(Jobs).filter(Jobs.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job not found. Id: {job_id}")
    try:
        db.delete(job)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Problem deleting job id {job_id}: {e}")


# truncate all company data
@app.delete("/restart-schema/", status_code=status.HTTP_200_OK)
async def restart_schema(db: db_dependency):
    """
    This endpoint restart the schema deleting all data
    """
    db.execute(sqltext("SET FOREIGN_KEY_CHECKS = 0"))
    db.execute(sqltext("TRUNCATE TABLE employees"))
    db.execute(sqltext("TRUNCATE TABLE departments"))
    db.execute(sqltext("TRUNCATE TABLE jobs"))
    db.execute(sqltext("SET FOREIGN_KEY_CHECKS = 1"))
    db.commit()


# load company data
@app.post("/load-employees/", status_code=status.HTTP_200_OK)
async def load_employees(employees: list, db: db_dependency):
    employees_list = json.loads("["+employees[0]+"]")
    if isinstance(employees_list[0], list):
        employees_list = employees_list[0]
    for index, emp in enumerate(employees_list):
        new_emp = Employees(**emp)
        db.add(new_emp)
        if math.remainder(index, 10) == 0:
            db.commit()
    db.commit()


@app.post("/load-departments/", status_code=status.HTTP_200_OK)
async def load_departments(departments: list, db: db_dependency):
    departments_list = json.loads("["+departments[0]+"]")
    if isinstance(departments_list[0], list):
        departments_list = departments_list[0]
    for index, dep in enumerate(departments_list):
        new_dep = Departments(**dep)
        db.add(new_dep)
        if math.remainder(index, 10) == 0:
            db.commit()
    db.commit()


@app.post("/load-jobs/", status_code=status.HTTP_200_OK)
async def load_jobs(jobs: list, db: db_dependency):
    jobs_list = json.loads("["+jobs[0]+"]")
    if isinstance(jobs_list[0], list):
        jobs_list = jobs_list[0]
    for index, job in enumerate(jobs_list):
        new_job = Jobs(**job)
        db.add(new_job)
        if math.remainder(index, 10) == 0:
            db.commit()
    db.commit()


@app.get("/kpi/{n_kpi}", status_code=status.HTTP_200_OK)
async def get_kpi(n_kpi: int, db: db_dependency):
    rows = db.execute(f"Select * from kpi{n_kpi}").fetchall()
    return rows


@app.get("/")
def company_root():
    return {"message": "I'm alive!!"}
