from test.util import make_weights
from mi_scale_2.notification import get_change_trend_message, get_averages_message
from mi_scale_2.config import CHANGE_TRENDS_DAYS

first_day = CHANGE_TRENDS_DAYS[0]

def test_get_change_trend_message_negative():
    weights = make_weights([60, 70])
    message = get_change_trend_message(weights)
    assert f"{first_day}: 📉-10" in message

def test_get_change_trend_message_positive():
    weights = make_weights([70, 60])
    message = get_change_trend_message(weights)
    assert f"{first_day}: 📈+10" in message


def test_get_averages_message_negative():
    weights = make_weights([60, 70])
    message = get_averages_message(weights)
    assert f"{first_day}: 📉65" in message

def test_get_averages_message_positive():
    weights = make_weights([70, 60])
    message = get_averages_message(weights)
    assert f"{first_day}: 📈65" in message
