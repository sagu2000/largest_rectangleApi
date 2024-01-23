from database import Base
from sqlalchemy import create_engine, Column, Integer, JSON, DateTime
from datetime import datetime
class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(Integer, primary_key=True, index=True)
    matrix = Column(JSON)
    area = Column(Integer, nullable=True)
    number = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    turnaround_time = Column(Integer, nullable=True)