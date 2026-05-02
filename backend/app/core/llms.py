import os
from langchain_anthropic import ChatAnthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_API_URL = os.getenv("ANTHROPIC_API_URL", "https://open.bigmodel.cn/api/anthropic")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

def get_default_model():
    return ChatAnthropic(
        model=ANTHROPIC_MODEL,
        max_tokens=8192,
        temperature=0.2,
        anthropic_api_url=ANTHROPIC_API_URL,
        anthropic_api_key=ANTHROPIC_API_KEY,
    )
