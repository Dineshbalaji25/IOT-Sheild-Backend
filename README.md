# IoT Monitoring Backend

Production-ready Python backend for an IoT monitoring platform using FastAPI, SQLAlchemy, MySQL, and MQTT.

## Features

- **Event-Driven Ingestion**: Continuously listen to MQTT sensor messages.
- **Data Validation**: Validate sensor data against predefined thresholds.
- **Persistence**: Store raw telemetry and alerts in MySQL.
- **REST API**: Comprehensive endpoints for history, latest readings, and statistics.
- **Dockerized**: Fully containerized setup with Docker Compose.

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy ORM
- MySQL
- Eclipse Mosquitto (MQTT Broker)
- Paho-MQTT
- Docker & Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.

### Installation & Setup

1. Clone the repository (if applicable) or navigate to the project directory.
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

The backend will automatically:
- Connect to the MySQL database and create the necessary tables.
- Connect to the Mosquitto broker and subscribe to the configured topics.
- Start the FastAPI server on [http://localhost:8000](http://localhost:8000).

### API Endpoints

- **Health Check**: `GET /health`
- **Latest Readings**: `GET /sensors/latest`
- **Telemetry History**: `GET /sensors/history?device_id=device_01&limit=50`
- **Alerts**: `GET /alerts`
- **Statistics**: `GET /stats`

### Threshold Rules

The service monitors the following thresholds:
- Temperature: 0 – 50°C
- Humidity: 10 – 90%
- Voltage: 200 – 240V
- Current: 0 – 10A
- Pressure: 900 – 1100 hPa

Any violation will trigger an alert stored in the `alerts` table.

## Architecture

```text
app/
├── main.py             # App entry point & lifespan management
├── api/
│   └── routes.py       # REST API endpoints
├── core/
│   └── config.py       # Configuration & environment variables
├── db/
│   └── session.py      # Database engine & session setup
├── models/
│   └── iot_models.py   # SQLAlchemy models
├── schemas/
│   └── iot_schemas.py  # Pydantic schemas (validation/response)
└── services/
    ├── alert_service.py   # Threshold validation & alert logic
    ├── mqtt_consumer.py   # Background MQTT ingestion service
    └── sensor_service.py  # Sensor data database operations
```

## MQTT Payload Example

Send a JSON payload to `sensors/device1`:

```json
{
  "device_id": "device_01",
  "temperature": 28.4,
  "humidity": 65.2,
  "voltage": 229.1,
  "current": 3.4,
  "pressure": 1008.5
}
```
