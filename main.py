from settings import logger
from core.model import get_agent

if __name__ == '__main__':
    input_msg = "新西兰基督城未来7天的天气如何？"
    agent = get_agent()
    response = agent.invoke(input_msg)
    logger.info(response)