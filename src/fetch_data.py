import os
import json
import logging
from typing import Dict, Any, Optional
import requests

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CITIES = {
    "Colombo": {"lat": 6.9271, "lon": 79.8612},
    "Kandy": {"lat": 7.2906, "lon": 80.6337},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "New_York": {"lat": 40.7128, "lon": -74.0060}
}

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def fetch_city_data(city_name: str, lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Fetch weather and air quality metrics for a given city coordinate."""
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "timezone": "auto"
    }
    
    air_params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide",
        "timezone": "auto"
    }

    try:
        logging.info(f"Fetching data for {city_name}...")
        weather_res = requests.get(WEATHER_API_URL, params=weather_params, timeout=10)
        air_res = requests.get(AIR_QUALITY_API_URL, params=air_params, timeout=10)

        weather_res.raise_for_status()
        air_res.raise_for_status()

        payload = {
            "city": city_name,
            "latitude": lat,
            "longitude": lon,
            "weather": weather_res.json(),
            "air_quality": air_res.json()
        }
        return payload

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data for {city_name}: {e}")
        return None


def save_raw_data(data: Dict[str, Any], output_dir: str = "data/raw") -> None:
    """Save raw JSON payload to disk."""
    os.makedirs(output_dir, exist_ok=True)
    city_name = data["city"].lower()
    filepath = os.path.join(output_dir, f"{city_name}_raw.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    logging.info(f"Saved raw payload to {filepath}")


def main():
    logging.info("Starting Weather & AQI Ingestion Pipeline...")
    for city, coords in CITIES.items():
        payload = fetch_city_data(city, coords["lat"], coords["lon"])
        if payload:
            save_raw_data(payload)
    logging.info("Ingestion complete.")


if __name__ == "__main__":
    main()