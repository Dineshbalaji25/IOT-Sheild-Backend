import json
import logging
import paho.mqtt.client as mqtt
from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.iot_schemas import SensorPayload
from app.services.sensor_service import SensorService
from app.services.alert_service import AlertService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MQTTConsumer:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker successfully")
            for topic in settings.topic_list:
                client.subscribe(topic)
                logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to MQTT Broker, return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logger.warning(f"Disconnected from MQTT Broker with code {rc}. Attempting reconnect...")

    def on_message(self, client, userdata, msg):
        try:
            payload_data = json.loads(msg.payload.decode())
            logger.info(f"Received message on {msg.topic}: {payload_data}")
            
            # Basic validation check for required fields before pydantic
            sensor_payload = SensorPayload(**payload_data)
            
            db = SessionLocal()
            try:
                # 1. Store raw telemetry
                SensorService.create_sensor_reading(db, sensor_payload, msg.topic)
                
                # 2. Check thresholds and create alerts
                AlertService.check_and_create_alerts(db, sensor_payload, msg.topic)
            finally:
                db.close()
                
        except json.JSONDecodeError:
            logger.error(f"Failed to decode message on {msg.topic}: {msg.payload}")
        except Exception as e:
            logger.error(f"Error processing message on {msg.topic}: {str(e)}")

    def start(self):
        try:
            self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
            self.client.loop_start()
            logger.info("MQTT Loop started")
        except Exception as e:
            logger.error(f"Could not connect to MQTT Broker: {str(e)}")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("MQTT Loop stopped")

mqtt_consumer = MQTTConsumer()
