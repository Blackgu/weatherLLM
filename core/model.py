from langchain_community.chat_models import ChatTongyi

def get_model():
    model = ChatTongyi(model="qwen-turbo",
                       top_p=1)
    return model