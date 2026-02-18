from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+mysqlconnector://user:userpassword@localhost:3306/iot_db"
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_TOPICS: str = "sensors/device1,sensors/device2,sensors/device3"
    
    # Thresholds
    TEMP_MIN: float = 0.0
    TEMP_MAX: float = 50.0
    HUMID_MIN: float = 10.0
    HUMID_MAX: float = 90.0
    VOLT_MIN: float = 200.0
    VOLT_MAX: float = 240.0
    CURR_MIN: float = 0.0
    CURR_MAX: float = 10.0
    PRESS_MIN: float = 900.0
    PRESS_MAX: float = 1100.0

    @property
    def topic_list(self) -> List[str]:
        return [t.strip() for t in self.MQTT_TOPICS.split(",")]

    class Config:
        env_file = ".env"

settings = Settings()
