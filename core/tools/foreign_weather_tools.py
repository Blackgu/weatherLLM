import json
import os

from langchain_core.tools import tool
from core.weather import (CURRENT_CONDITION_URL, FORECAST_DAYS_URL, make_weather_request)

GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")

@tool
def get_current_condition_weather(latitude: float, longitude: float) -> str | None:
    """
    查询城市地区（除中国外的其他国家）的当天的天气情况
    Args:
        latitude: 纬度，例如：39.90403
        longitude: 经度，例如：116.407526
    Returns:
        返回包含当前天气信息的字符串
    """
    url = f"{CURRENT_CONDITION_URL}?key={GEMINI_API_KEY}&location.latitude={latitude}&location.longitude={longitude}"
    data = make_weather_request(url)
    if not data:
        return "Unable to fetch current weather data."
    return json.dumps(data)

@tool
def get_tomorrow_weather(latitude: float, longitude: float) -> str:
    """
    查询城市地区（除中国外的其他国家）的明天的天气预报
    Args:
        latitude: 纬度，例如：39.90403
        longitude: 经度，例如：116.407526
        days: 需要获取的天数，默认为3
    Returns:
        返回包含未来天气预报信息的字符串
    """
    url = f"{FORECAST_DAYS_URL}?key={GEMINI_API_KEY}&location.latitude={latitude}&location.longitude={longitude}&days=2"
    data = make_weather_request(url)
    if not data:
        return "Unable to fetch forecast weather data."

    tomorrow_cast = data["forecastDays"][1]
    return json.dumps(tomorrow_cast)

@tool
def get_forecast_weather(latitude: float, longitude: float, days: int = 3) -> str | None:
    """
    查询城市地区（除中国外的其他国家）的未来几天的天气预报
    Args:
        latitude: 纬度，例如：39.90403
        longitude: 经度，例如：116.407526
        days: 需要获取的天数，默认为3
    Returns:
        返回包含未来天气预报信息的字符串
    """
    url = f"{FORECAST_DAYS_URL}?key={GEMINI_API_KEY}&location.latitude={latitude}&location.longitude={longitude}&days={days}"
    data = make_weather_request(url)
    if not data:
        return "Unable to fetch forecast weather data."
    return json.dumps(data)

# @tool
# def get_forecast_weather_date(latitude: float, longitude: float, date: datetime) -> str | None:
#     """
#     查询非中国城市地区的指定日期的天气情况
#     Args:
#         latitude: 纬度，例如：39.90403
#         longitude: 经度，例如：116.407526
#         date: 指定的日期，例如：2023-07-01
#     Returns:
#         返回包含指定日期的天气信息的字符串
#     """
#     internal_days = (date - datetime.today()).days
#
#     url = (f"{FORECAST_DAYS_URL}?key={GEMINI_API_KEY}&location.latitude={latitude}"
#            f"&location.longitude={longitude}&days={internal_days}")
#
#     data = make_weather_request(url)
#     if not data:
#         return "Unable to fetch forecast weather data."
#
#     forecastDays = data["forecastDays"]
#     for forecast in forecastDays:
#         date_str = date.strftime("%Y-%m-%dT%H:%M:%S%zZ")
#         start_time = forecast["interval"]["startTime"]
#         end_time = forecast["interval"]["endTime"]
#         if date_str == start_time or date_str == end_time:
#             return json.dumps(forecast)
#     return None
