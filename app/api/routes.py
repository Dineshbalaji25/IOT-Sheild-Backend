from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.session import get_db
from app.services.sensor_service import SensorService
from app.services.alert_service import AlertService
from app.schemas.iot_schemas import SensorResponse, AlertResponse, StatsResponse

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/sensors/latest", response_model=List[SensorResponse])
def get_latest_sensors(db: Session = Depends(get_db)):
    return SensorService.get_latest_readings(db)

@router.get("/sensors/history", response_model=List[SensorResponse])
def get_sensor_history(
    device_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    return SensorService.get_history(db, device_id, start_time, end_time, skip, limit)

@router.get("/alerts", response_model=List[AlertResponse])
def get_alerts(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    return AlertService.get_all_alerts(db, limit)

@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    return {
        "total_messages": SensorService.get_total_count(db),
        "total_alerts": AlertService.get_total_alerts_count(db),
        "active_devices": SensorService.get_active_devices_count(db)
    }
