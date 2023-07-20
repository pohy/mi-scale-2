import requests

from mi_scale_2.logger import log
from mi_scale_2.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from mi_scale_2.weight_util import get_change_average, get_change_trend, get_saved_weights

token = TELEGRAM_BOT_TOKEN
chat_id = TELEGRAM_CHAT_ID
change_trends_days_since_now = [7, 14, 30, 90]

def send_notification(weight):
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
    weights = get_saved_weights()
    if len(weights) == 0:
        return "No weight data"
    averages = []
    for day in change_trends_days_since_now:
        average = get_change_average(weights, day)
        if average is None:
            average = "?"
        else:
            average = round(average, 2)
        averages.append(format_series_entry(day, average))
    return format_series_message("Average by day", averages)

def get_change_trend_message():
    weights = get_saved_weights()
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
        trends.append(format_series_entry(day, trend))
    return format_series_message("Trend by day", trends)

def format_series_entry(key, value):
    return f"{key}: {value}kg"

def format_series_message(msg, series):
    str = "  |  ".join(series)
    return f"{msg}:\n{str}"


