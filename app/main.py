from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.api.routes import router as api_router
from app.services.mqtt_consumer import mqtt_consumer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting up IoT Backend...")
    
    # 1. Create database tables if they don't exist
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

    # 2. Start MQTT Consumer
    mqtt_consumer.start()
    logger.info("MQTT Consumer initialized.")

    yield

    # Shutdown logic
    logger.info("Shutting down IoT Backend...")
    mqtt_consumer.stop()

app = FastAPI(
    title="IoT Shield Monitoring Platform",
    description="Event-driven telemetry ingestion and alerting service.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
