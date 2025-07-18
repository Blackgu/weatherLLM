from typing import Any
import httpx

BASE_URL = "https://restapi.amap.com/v3/weather/weatherInfo"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception:
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

def format_forecast(forecast: dict) -> str:
    """
    Format an alert feature into a readable string.
    """
    casts = forecast['casts']

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