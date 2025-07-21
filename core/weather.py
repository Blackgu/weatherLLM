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

def format_alert(live: dict) -> str:
    """
    Format an alert feature into a readable string.
    """
    return f"""
    Area: {live.get('province', 'Unknown')} + "-" + {live.get('city', 'Unknown')}
    Weather: {live.get('weather', 'Unknown')}
    Temperature: {live.get('temperature', 'Unknown')}
    Wind-direction: {live.get('winddirection', 'Unknown')}
    Windpower: {live.get('windpower', 'Unknown')}
    Humidity: {live.get('humidity', 'Unknown')}
    """

def format_forecast(forecast: dict, days: int = 3) -> str:
    """
    Format an alert feature into a readable string.
    """
    casts = forecast['casts'][:days]

    result = f"""
    Area: {forecast.get('province', 'Unknown')} + "-" + {forecast.get('city', 'Unknown')}
    """
    for cast in casts:
        result += f"""
        Date: {cast.get('date', 'Unknown')} {cast.get('week', 'Unknown')}
        DayWeather: {cast.get('dayweather', 'Unknown')} {cast.get('daytemp', 'Unknown')}
        DayWind: {cast.get('daywind', 'Unknown')} {cast.get('daypower', 'Unknown')}
        NightWeather: {cast.get('nightweather', 'Unknown')} {cast.get('nighttemp', 'Unknown')}
        NightWind: {cast.get('nightwind', 'Unknown')} {cast.get('nightpower', 'Unknown')}
        """

    return result