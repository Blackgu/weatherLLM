from langchain.chat_models import init_chat_model

def get_model():
    model = init_chat_model("gpt-4o-mini",
                            temperature=1.0,
                            model_provider="openai")
    return model