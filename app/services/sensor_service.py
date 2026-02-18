from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.iot_models import SensorData
from app.schemas.iot_schemas import SensorPayload
from datetime import datetime, timezone

class SensorService:
    @staticmethod
    def create_sensor_reading(db: Session, payload: SensorPayload, topic: str):
        db_reading = SensorData(
            device_id=payload.device_id,
            topic=topic,
            temperature=payload.temperature,
            humidity=payload.humidity,
            voltage=payload.voltage,
            current=payload.current,
            pressure=payload.pressure,
            received_at=datetime.now(timezone.utc)
        )
        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)
        return db_reading

    @staticmethod
    def get_latest_readings(db: Session):
        # Subquery to find the maximum received_at for each device_id
        subquery = db.query(
            SensorData.device_id,
            func.max(SensorData.received_at).label('max_received_at')
        ).group_by(SensorData.device_id).subquery()

        # Join the subquery with the original table to get the full records
        query = db.query(SensorData).join(
            subquery,
            (SensorData.device_id == subquery.c.device_id) &
            (SensorData.received_at == subquery.c.max_received_at)
        )
        return query.all()

    @staticmethod
    def get_history(db: Session, device_id: str = None, topic: str = None, start_time: datetime = None, end_time: datetime = None, skip: int = 0, limit: int = 100):
        query = db.query(SensorData)
        if device_id:
            query = query.filter(SensorData.device_id == device_id)
        if topic:
            query = query.filter(SensorData.topic == topic)
        if start_time:
            query = query.filter(SensorData.received_at >= start_time)
        if end_time:
            query = query.filter(SensorData.received_at <= end_time)
        
        return query.order_by(SensorData.received_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_total_count(db: Session):
        return db.query(func.count(SensorData.id)).scalar()

    @staticmethod
    def get_active_devices_count(db: Session):
        return db.query(func.count(func.distinct(SensorData.device_id))).scalar()
