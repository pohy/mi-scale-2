import requests
from logger import log
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from weight_util import get_change_average, get_change_trend, get_weights

token = TELEGRAM_BOT_TOKEN
chat_id = TELEGRAM_CHAT_ID
change_trends_days_since_now = [1, 5, 15, 30, 90]

def send(weight):
    if token is None or chat_id is None:
        log.warn("telegram token or chat id not set")
        return
    trend = get_change_trend_message()
    average = get_averages_message()
    message = f"New weight recorded: {weight} kg\n{trend}\n{average}"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url).json()
    log.debug("sent telegram notification", response)

def get_averages_message():
    weights = get_weights()
    if len(weights) == 0:
        return "No weight data"
    averages = []
    for day in change_trends_days_since_now:
        average = get_change_average(weights, day)
        if average is None:
            average = "?"
        else:
            average = round(average, 2)
        averages.append(f"{day} days: {average}")
    averages_str = " | ".join(averages)
    return f"Averages: {averages_str}"

def get_change_trend_message():
    weights = get_weights()
    if len(weights) == 0:
        return "No weight data"
    trends = []
    for day in change_trends_days_since_now:
        trend = get_change_trend(weights, day)
        if trend is None:
            trend = "?"
        else:
            is_positive = trend > 0
            trend = round(trend, 2)
            trend = f"+{trend}" if is_positive else trend
        trends.append(f"{day} days: {trend}")
    trends_str = " | ".join(trends)
    return f"Trends: {trends_str}"


