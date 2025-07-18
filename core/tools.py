import os
from langchain_core.tools import tool
from core.weather import BASE_URL, make_nws_request, format_alert, format_forecast
from core.division import init_city_codes

GAODE_ACCESS_KEY = '819e27eccea420a48463e6f63f0386b5'

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "data", "AMap_adcode_citycode.xlsx")


divisions = init_city_codes(file_path)

def get_citycode(city_name: str) -> str:
    """
    根据城市名称获取对应的行政区划编码。

    参数:
    city_name (str): 要查找的城市名称。

    返回:
    str: 对应的行政区划编码，如果未找到则返回 None。

    功能:
    遍历所有行政区划名称，如果找到完全匹配或包含关系的行政区划，则返回其编码。
    """
    for division_name, division in divisions.items():
        if city_name == division_name or city_name in division_name:
            return division.adcode
    return None

@tool
def get_alerts(city_name: str) -> str:
    """
    查询输入城市的当天的天气情况
    Args:
        city_name: 城市名称，例如：北京市
    """

    url = f"{BASE_URL}?key={GAODE_ACCESS_KEY}&city={get_citycode(city_name)}&extensions=base"
    data = make_nws_request(url)

    if not data or "lives" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["lives"]:
        return "No active alerts for this state."

    alerts = [format_alert(live) for live in data["lives"]]
    return "\n---\n".join(alerts)

@tool
def get_forecast(city_name: str) -> str:
    """
    获取输入城市未来三天的天气预报
    Args:
        city_name: 城市名称，例如：北京市
    """
    # First get the forecast grid endpoint
    url = f"{BASE_URL}?key={GAODE_ACCESS_KEY}&city={get_citycode(city_name)}&extensions=all"
    data = make_nws_request(url)

    if not data or "forecasts" not in data:
        return "Unable to fetch alerts or no alerts found."

    forecast = format_forecast(data["forecasts"][0])
    return "\n---\n".join(forecast)