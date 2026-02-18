import json
import time
import random
import paho.mqtt.client as mqtt

# Configuration
BROKER = "mosquitto"
PORT = 1883
TOPICS = [
    "sensors/device1",
    "sensors/device2",
    "sensors/device3",
    "sensors/device4",
    "sensors/device5"
]

def generate_sensor_data(device_id):
    # Generating some data, occasionally breaching thresholds
    return {
        "device_id": device_id,
        "temperature": round(random.uniform(15.0, 60.0), 2),  # Threshold Max 50.0
        "humidity": round(random.uniform(5.0, 95.0), 2),     # Threshold Min 10.0, Max 90.0
        "voltage": round(random.uniform(190.0, 250.0), 2),   # Threshold Min 200.0, Max 240.0
        "current": round(random.uniform(0.0, 12.0), 2),      # Threshold Max 10.0
        "pressure": round(random.uniform(850.0, 1150.0), 2)  # Threshold Min 900.0, Max 1100.0
    }

def run_simulator():
    client = mqtt.Client()
    try:
        client.connect(BROKER, PORT, 60)
        print(f"Connected to MQTT Broker at {BROKER}:{PORT}")
        
        while True:
            for topic in TOPICS:
                device_id = topic.split("/")[-1]
                data = generate_sensor_data(device_id)
                payload = json.dumps(data)
                
                client.publish(topic, payload)
                print(f"Published to {topic}: {payload}")
                
            time.sleep(5)  # Send every 5 seconds
    except Exception as e:
        print(f"Error in simulator: {e}")
    finally:
        client.disconnect()

if __name__ == "__main__":
    run_simulator()
