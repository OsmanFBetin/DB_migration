from sqlalchemy import Column, Integer, String
from db.database import Base

class HistoricalData(Base):
    __tablename__ = "historical_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    value = Column(Integer)
