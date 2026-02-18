from pydantic import BaseModel
from datetime import datetime
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

    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    total_messages: int
    total_alerts: int
    active_devices: int
