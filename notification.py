import os
import requests
from logger import log
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

token = TELEGRAM_BOT_TOKEN
chat_id = TELEGRAM_CHAT_ID

def send(weight):
    if token is None or chat_id is None:
        log.warn("telegram token or chat id not set")
        return
    message = f"New weight recorded: {weight} kg"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url).json()
    log.debug("sent telegram notification", response)
