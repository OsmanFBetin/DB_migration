from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
import datetime
class DepartmentData(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    department = Column(String)

class JobData(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    job = Column(String)

class HiredEmployeeData(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    datetime = Column(DateTime, nullable=True)
    department_id = Column(Integer, nullable=True)
    job_id = Column(Integer, nullable=True)

class EmployeeStats(Base):
    __tablename__ = "stats_employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    department = Column(String)
    job = Column(String)
    Q1 = Column(Integer)
    Q2 = Column(Integer)
    Q3 = Column(Integer)
    Q4 = Column(Integer)