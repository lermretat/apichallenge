from sqlalchemy import Column, Integer, String
from mysql_database import Base


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300))
    datetime = Column(String(45), index=True)
    department_id = Column(Integer)
    job_id = Column(Integer)


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String(100))


class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String(100))
