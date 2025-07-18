import getpass
import os
import logging

from dotenv import load_dotenv

try:
    load_dotenv(verbose=True)
except ImportError:
    pass

if "LANGSMITH_TRACING" not in os.environ:
    os.environ["LANGSMITH_API_KEY"] = getpass.getpass(
        prompt="Please enter your LangSmith tracing config: "
    )

if "LANGSMITH_API_KEY" not in os.environ:
    os.environ["LANGSMITH_API_KEY"] = getpass.getpass(
        prompt="Please enter your LangSmith API key: "
    )

if "LANGSMITH_PROJECT_NAME" not in os.environ:
    os.environ["LANGSMITH_PROJECT_NAME"] = getpass.getpass(
        prompt="Please enter your LangSmith project name: "
    )

if "DASHSCOPE_API_KEY" not in os.environ:
    os.environ["DASHSCOPE_API_KEY"] = getpass.getpass(
        prompt="Please enter your DASHSCOPE API key: "
    )