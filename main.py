from settings import logger
from core.tools import get_alerts, get_forecast
from core.model import get_model
from langchain_core.messages import HumanMessage

model = get_model()
tools = [get_alerts, get_forecast]
model_with_tools = model.bind_tools(tools=tools)

if __name__ == '__main__':
    query = "北京今天天气如何？"
    messages = [HumanMessage(content=query)]

    ai_msg = model_with_tools.invoke(messages)
    print(ai_msg.tool_calls)
    messages.append(ai_msg)
    print(messages)