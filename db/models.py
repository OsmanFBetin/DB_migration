from sqlalchemy import Column, Integer, String
from db.database import Base

class HistoricalData(Base):
    # __tablename__ = "historical_data"
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)
    # value = Column(Integer)
