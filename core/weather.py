import os
from typing import Any
from settings import logger
import httpx

GAODE_BASE_URL = "https://restapi.amap.com/v3/weather/weatherInfo"
CURRENT_CONDITION_URL = "https://weather.googleapis.com/v1/currentConditions:lookup"
FORECAST_DAYS_URL = "https://weather.googleapis.com/v1/forecast/days:lookup"
FORECAST_HOURS_URL = "https://weather.googleapis.com/v1/forecast/hours:lookup"
USER_AGENT = "weather-llm/1.0"

def make_weather_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Google API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }

    with httpx.Client() as client:
        try:
            response = client.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception:
            logger.error(f"Error making request to GOOGLE API: {url}")
            return None