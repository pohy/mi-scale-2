from os import path
from dotenv import dotenv_values

config_path = path.join(path.dirname(__file__), "..", ".env")
config = dotenv_values(config_path)

ENV = config.get("ENV", "development")
IS_PRODUCTION = ENV == "production"
PORT = config.get("PORT", 80 if IS_PRODUCTION else 1337)
PORT = int(PORT)
LOG_LEVEL = config.get("LOG_LEVEL", "info")

MAC_ADDRESS = config.get("MAC_ADDRESS", None)
TIMEOUT = config.get("TIMEOUT", 0.2)
MIN_WEIGHT = config.get("MIN_WEIGHT", 0.0)
MAX_WEIGHT = config.get("MAX_WEIGHT", 90.0)

TELEGRAM_BOT_TOKEN = config.get("TELEGRAM_BOT_TOKEN", None)
TELEGRAM_CHAT_ID = config.get("TELEGRAM_CHAT_ID", None)

