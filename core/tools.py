import os
from langchain_core.tools import tool
from core.weather import BASE_URL, make_nws_request, format_alert, format_forecast
from core.division import init_city_codes

GAODE_ACCESS_KEY = os.getenv("GAODE_ACCESS_KEY")

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "data", "AMap_adcode_citycode.xlsx")


divisions = init_city_codes(file_path)

def get_citycode(city_name: str, division_name: str) -> str:
    """
    根据城市名称获取对应的行政区划编码。

    参数:
    city_name (str): 要查找的城市名称。例如：北京市
    division_name (str): 要查找的城市区域名称。例如：东城区

    返回:
    str: 对应的行政区划编码，如果未找到则返回 None。

    功能:
    遍历所有行政区划名称，如果找到完全匹配或包含关系的行政区划，则返回其编码。
    """
    if city_name is None:
        return None

    if division_name is None:
        for address_name, division in divisions.items():
            if city_name == address_name or city_name in address_name:
                return division.adcode

    for address_name, division in divisions.items():
        if "-" in address_name:
            addr_city_name, addr_division_name = address_name.split("-")
            if ((city_name == addr_city_name or city_name in addr_city_name)
                    and (division_name == addr_division_name or division_name in addr_division_name)):
                return division.adcode
    return None

@tool
def get_alerts_city(city_name: str) -> str:
    """
    查询输入城市的当天的天气情况
    Args:
        city_name: 城市名称，例如：北京市
    """
    return get_alerts_address.invoke(city_name)

@tool
def get_alerts_address(city_name: str, division_name: str = None) -> str:
    """
    查询输入城市的当天的天气情况
    Args:
        city_name: 城市名称，例如：北京市
        division_name: 城市的区域名称（例如：东城区），如果没有询问具体区域，则可以为空
    """

    url = f"{BASE_URL}?key={GAODE_ACCESS_KEY}&city={get_citycode(city_name, division_name)}&extensions=base"
    data = make_nws_request(url)

    if not data or "lives" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["lives"]:
        return "No active alerts for this state."

    alerts = [format_alert(live) for live in data["lives"]]
    return "\n---\n".join(alerts)

@tool
def get_forecast_city(city_name: str, days: int = 3) -> str:
    """
    查询输入城市的未来几天的天气情况
    Args:
        city_name: 城市名称，例如：北京市
        days: 需要获取的天数，默认为3天
    """
    return get_forecast_address.invoke(city_name, days)

@tool
def get_forecast_address(city_name: str, division_name: str = None, days: int = 3) -> str:
    """
    获取输入城市未来指定天数的天气预报

    Args:
        city_name: 城市名称，例如：北京市
        division_name: 城市的区域名称（例如：东城区），如果没有询问具体区域，则可以为空
        days: 需要获取的未来天数，默认为3天

    Returns:
        返回包含未来天气预报信息的字符串
    """

    adcode = get_citycode(city_name, division_name)
    if adcode is None:
        return "Unable to get citycode. city_name=" + city_name

    # 构建请求URL，包含基础URL、高德API访问密钥和城市编码
    url = f"{BASE_URL}?key={GAODE_ACCESS_KEY}&city={adcode}&extensions=all"

    # 发起网络请求获取天气数据
    data = make_nws_request(url)

    # 判断获取的数据是否为空或者不包含预报信息
    if not data or "forecasts" not in data:
        return "Unable to fetch alerts or no alerts found."

    # 格式化预报数据，截取指定天数的预报信息
    forecast = format_forecast(data["forecasts"][0], days)

    # 将格式化后的预报信息以换行符连接成最终返回结果
    return "\n---\n".join(forecast)
