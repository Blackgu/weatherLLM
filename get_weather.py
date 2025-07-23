import gradio as gr
from settings import logger

from core.model import get_agent

agent = get_agent()
def forecast_weather(message, chat_history):

    # 确保聊天历史格式正确
    if not isinstance(chat_history, list):
        chat_history = []

    response = agent.invoke(message)
    logger.info(response)

    return {"role": "assistant", "content": response.get("output", "")}

demo = gr.ChatInterface(
    forecast_weather,
    type="messages"
)

demo.launch()