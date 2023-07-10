import os
from dotenv import dotenv_values
import requests
from logger import log

config = dotenv_values(os.path.dirname(__file__) + "/.env")

token = config.get("TELEGRAM_BOT_TOKEN", None)
chat_id = config.get("TELEGRAM_CHAT_ID", None)

def send(weight):
    if token is None or chat_id is None:
        log.warn("telegram token or chat id not set")
        return
    message = f"New weight recorded: {weight} kg"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url).json()
    log.debug("sent telegram notification", response)
