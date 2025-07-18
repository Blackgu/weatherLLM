from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatTongyi

def get_model():
    model = ChatTongyi(model="qwen-turbo",
                       temperature=1,
                       api_key="sk-28d446d86f2a4b23ab1902c9621f2d51")
    return model