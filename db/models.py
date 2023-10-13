from sqlalchemy import Column, Integer, String
from db.database import Base

class HistoricalData(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    department = Column(String)
