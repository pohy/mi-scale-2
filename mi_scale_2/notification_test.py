from test.util import make_weights
from mi_scale_2.notification import get_change_trend_message, get_change_trend_message

def test_get_change_trend_message_negative():
    weights = make_weights([60, 70])
    message = get_change_trend_message(weights)
    assert "📉-10" in message

def test_get_change_trend_message_positive():
    weights = make_weights([70, 60])
    message = get_change_trend_message(weights)
    assert "📈+10" in message

