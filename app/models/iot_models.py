from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from app.db.session import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(50), index=True)
    topic = Column(String(100))
    temperature = Column(Float)
    humidity = Column(Float)
    voltage = Column(Float)
    current = Column(Float)
    pressure = Column(Float)
    received_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(50), index=True)
    topic = Column(String(100))
    violated_parameters = Column(String(255))  # Or JSON if mysql supports it well, user said string or JSON
    actual_values = Column(JSON)
    message_timestamp = Column(DateTime)
    alert_created_at = Column(DateTime, default=datetime.utcnow)
