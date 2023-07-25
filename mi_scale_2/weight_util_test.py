from datetime import datetime, timedelta
from test.util import make_weights
import pytest

from mi_scale_2.weight_util import get_change_average, get_change_trend, get_changed_weights_since


@pytest.fixture
def weights():
    weight_entries = [60, 70, 80, 90, 100]
    return make_weights(weight_entries)

def test_get_change_trend_returns_float(weights):
    trend = get_change_trend(weights, 1)
    print(type(trend))
    assert isinstance(trend, float)

def test_get_change_trend_returns_positive():
    weights = make_weights([70, 60])
    trend = get_change_trend(weights, 3)
    assert trend == 10

def test_get_change_trend_1_day(weights):
    trend = get_change_trend(weights, 1)
    assert trend == 0

def test_get_change_trend_3_day(weights):
    trend = get_change_trend(weights, 3)
    assert trend == -20

def test_get_change_trend_5_day(weights):
    trend = get_change_trend(weights, 5)
    assert trend == -40

def test_get_change_average_1_day(weights):
    average = get_change_average(weights, 1)
    assert average == 60

def test_get_change_average_3_day(weights):
    average = get_change_average(weights, 3)
    assert average == 70

def test_get_change_average_5_day(weights):
    average = get_change_average(weights, 5)
    assert average == 80

def test_get_changed_weights_since_1_day(weights):
    changed_weights = get_changed_weights_since(weights, datetime.now() - timedelta(days=1))
    assert changed_weights == weights[:1]
    
def test_get_changed_weights_since_3_days(weights):
    changed_weights = get_changed_weights_since(weights, datetime.now() - timedelta(days=3))
    assert changed_weights == weights[:3]
