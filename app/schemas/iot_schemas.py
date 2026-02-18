from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

class SensorPayload(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    voltage: float
    current: float
    pressure: float

class SensorResponse(SensorPayload):
    id: int
    topic: str
    received_at: datetime

    @field_validator('received_at', mode='before')
    @classmethod
    def ensure_utc(cls, v):
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    class Config:
        from_attributes = True

class AlertResponse(BaseModel):
    id: int
    device_id: str
    topic: str
    violated_parameters: str
    actual_values: Dict[str, Any]
    message_timestamp: datetime
    alert_created_at: datetime

    @field_validator('message_timestamp', 'alert_created_at', mode='before')
    @classmethod
    def ensure_utc(cls, v):
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    total_messages: int
    total_alerts: int
    active_devices: int
