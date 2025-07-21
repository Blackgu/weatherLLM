from settings import logger
from core.tools import get_forecast_weather, get_current_condition_weather
from core.china_tools import get_china_alerts_city, get_china_alerts_address, get_china_forecast_city, get_china_forecast_address
from core.model import get_model
from langchain_core.messages import HumanMessage

model = get_model()
tools = [get_forecast_weather, get_current_condition_weather,
         get_china_alerts_city, get_china_alerts_address,
         get_china_forecast_city, get_china_forecast_address]
model_with_tools = model.bind_tools(tools=tools)

if __name__ == '__main__':
    query = "美国纽约明天的天气如何？"
    messages = [HumanMessage(content=query)]

    ai_msg = model_with_tools.invoke(messages)
    logger.info(ai_msg.tool_calls)
    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {"get_forecast_weather": get_forecast_weather,
                         "get_current_condition_weather": get_current_condition_weather,
                         "get_china_alerts_city": get_china_alerts_city,
                         "get_china_alerts_address": get_china_alerts_address,
                         "get_china_forecast_city": get_china_forecast_city,
                         "get_china_forecast_address": get_china_forecast_address}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    response = model_with_tools.invoke(messages)
    logger.info(response.content)