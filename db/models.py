from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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
    department_id = Column(Integer, ForeignKey("departments.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    depto_r = relationship("departments", back_populates="hired_employees")
    jobs_r = relationship("jobs", back_populates="hired_employees")
