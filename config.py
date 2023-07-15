import os
from dotenv import dotenv_values

config = dotenv_values(os.path.dirname(__file__) + "/.env")

MAC_ADDRESS = config.get("MAC_ADDRESS", None)
TIMEOUT = config.get("TIMEOUT", 0.2)
MIN_WEIGHT = config.get("MIN_WEIGHT", 0.0)
MAX_WEIGHT = config.get("MAX_WEIGHT", 90.0)

TELEGRAM_BOT_TOKEN = config.get("TELEGRAM_BOT_TOKEN", None)
TELEGRAM_CHAT_ID = config.get("TELEGRAM_CHAT_ID", None)
