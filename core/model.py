from langchain_community.chat_models import ChatTongyi
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from core.tools import get_forecast_weather, get_current_condition_weather, get_tomorrow_weather
from core.china_tools import (get_china_alerts_city, get_china_alerts_address,
                              get_china_forecast_city, get_china_forecast_address)

tools = [get_forecast_weather, get_current_condition_weather, get_tomorrow_weather,
         get_china_alerts_city, get_china_alerts_address,
         get_china_forecast_city, get_china_forecast_address]

tongyi_llm = ChatTongyi(model="qwen-plus-2025-07-14", top_p=1)
CUSTOM_PROMPT = PromptTemplate.from_template(open("files/prompt.txt").read())

def get_agent() -> AgentExecutor:
    """
    创建并返回一个配置好的AgentExecutor实例

    参数:
        无

    返回:
        AgentExecutor: 配置好的智能体执行器，包含以下配置:
            - 使用STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION类型的ReAct策略
            - 启用详细日志输出
            - 自动处理解析错误
            - 使用自定义PromptTemplate

    包含的配置参数:
        tools: 工具列表
        tongyi_llm: 大语言模型实例
        CUSTOM_PROMPT: 自定义的提示模板
    """
    agent = initialize_agent(
        tools=tools,
        llm=tongyi_llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # 使用默认的 ReAct 策略
        verbose=True,  # 显示思考过程
        handle_parsing_errors=True,  # 自动处理解析错误
        agent_kwargs = {
            "prompt": CUSTOM_PROMPT  # 使用自定义的 PromptTemplate
        }
    )
    return agent
