from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.iot_models import Alert
from app.schemas.iot_schemas import SensorPayload
from app.core.config import settings
from datetime import datetime, timezone
import json
import logging

logger = logging.getLogger(__name__)

class AlertService:
    @staticmethod
    def check_and_create_alerts(db: Session, payload: SensorPayload, topic: str):
        violations = []
        
        if not (settings.TEMP_MIN <= payload.temperature <= settings.TEMP_MAX):
            violations.append("temperature")
        if not (settings.HUMID_MIN <= payload.humidity <= settings.HUMID_MAX):
            violations.append("humidity")
        if not (settings.VOLT_MIN <= payload.voltage <= settings.VOLT_MAX):
            violations.append("voltage")
        if not (settings.CURR_MIN <= payload.current <= settings.CURR_MAX):
            violations.append("current")
        if not (settings.PRESS_MIN <= payload.pressure <= settings.PRESS_MAX):
            violations.append("pressure")

        if violations:
            alert = Alert(
                device_id=payload.device_id,
                topic=topic,
                violated_parameters=", ".join(violations),
                actual_values=payload.model_dump(),
                message_timestamp=datetime.now(timezone.utc),
                alert_created_at=datetime.now(timezone.utc)
            )
            db.add(alert)
            db.commit()
            db.refresh(alert)
            logger.warning(f"ALERT TRIGGERED: Device {payload.device_id} on topic {topic}. Violations: {alert.violated_parameters}")
            return alert
        return None

    @staticmethod
    def get_all_alerts(db: Session, limit: int = 100):
        return db.query(Alert).order_by(Alert.alert_created_at.desc()).limit(limit).all()

    @staticmethod
    def get_total_alerts_count(db: Session):
        return db.query(func.count(Alert.id)).scalar()
