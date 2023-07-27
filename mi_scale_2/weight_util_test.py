from datetime import datetime, timedelta
from pandas.testing import assert_frame_equal
import pytest

from mi_scale_2.weight_util import get_change_trend, get_changed_weights_since
from test.util import make_weights


@pytest.fixture
def weights():
    weight_entries = [60, 65, 70, 75, 80, 85, 90]
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
    assert trend == -5

def test_get_change_trend_3_day(weights):
    trend = get_change_trend(weights, 3)
    assert trend == -15

def test_get_change_trend_5_day(weights):
    print('weigths', weights)
    trend = get_change_trend(weights, 5)
    assert trend == -25

def test_get_changed_weights_since_1_day(weights):
    changed_weights = get_changed_weights_since(weights, 1)
    assert_frame_equal(changed_weights, weights[:1])

    
def test_get_changed_weights_since_3_days(weights):
    changed_weights = get_changed_weights_since(weights, 3)
    assert_frame_equal(changed_weights, weights[:3])
