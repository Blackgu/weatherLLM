from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatTongyi
from openai import project


def get_model():
    model = ChatTongyi(model="qwen-turbo",
                       temperature=1,
                       project="weatherLLM")
    return model