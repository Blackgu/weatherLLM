from settings import logger
from core.tools import get_alerts, get_forecast
from core.model import get_model
from langchain_core.messages import HumanMessage

model = get_model()
tools = [get_alerts, get_forecast]
model_with_tools = model.bind_tools(tools=tools)

if __name__ == '__main__':
    query = "杭州未来3天的天气如何？"
    messages = [HumanMessage(content=query)]

    ai_msg = model_with_tools.invoke(messages)
    logger.info(ai_msg.tool_calls)
    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {"get_alerts": get_alerts, "get_forecast": get_forecast}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    response = model_with_tools.invoke(messages)
    logger.info(response.content)