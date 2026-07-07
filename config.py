"""
Configuration — loads from environment variables with sensible defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Twitter API v2
    TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY", "")
    TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET", "")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")

    # xAI (Grok)
    XAI_API_KEY = os.getenv("XAI_API_KEY", "")
    XAI_MODEL = os.getenv("XAI_MODEL", "grok-4-1-fast-reasoning")

    # Bot
    BOT_USERNAME = os.getenv("BOT_USERNAME", "zagentics")
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "30"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.9"))
    MAX_REPLY_LENGTH = int(os.getenv("MAX_REPLY_LENGTH", "280"))

    # Persistence
    REPLIED_IDS_FILE = os.getenv("REPLIED_IDS_FILE", "data/replied_ids.json")
