from datetime import datetime, timezone
import random

from fastapi import FastAPI, Query

app = FastAPI()


def resolve_location_and_sensor_id(location: str, sensor_id: str):
    if not location:
        location = {
            "1": "Living Room",
            "2": "Bedroom",
            "3": "Kitchen",
        }.get(sensor_id, "Unknown")

    if not sensor_id:
        sensor_id = {
            "Living Room": "1",
            "Bedroom": "2",
            "Kitchen": "3",
        }.get(location, "0")

    return location, sensor_id


def build_temperature_response(location: str, sensor_id: str):
    value = round(random.uniform(18.0, 30.0), 1)
    return {
        "value": value,
        "unit": "C",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": location,
        "status": "active",
        "sensor_id": sensor_id,
        "sensor_type": "temperature",
        "description": f"Temperature in {location}",
    }


@app.get("/temperature")
def get_temperature(
    location: str = Query(default=""),
    sensorId: str = Query(default="", alias="sensorId"),
):
    location, sensor_id = resolve_location_and_sensor_id(location, sensorId)
    return build_temperature_response(location, sensor_id)


@app.get("/temperature/{sensor_id}")
def get_temperature_by_sensor_id(sensor_id: str):
    location, sensor_id = resolve_location_and_sensor_id("", sensor_id)
    return build_temperature_response(location, sensor_id)
