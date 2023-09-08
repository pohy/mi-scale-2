import os
from datetime import datetime, timedelta
from pandas.testing import assert_frame_equal
import pytest

from mi_scale_2.weight_util import get_change_trend, get_changed_weights_since, report_weight, get_saved_weights_list
from mi_scale_2.config import DATA_DIR
from test.util import make_weights


@pytest.fixture
def weights():
    weight_entries = [60, 65, 70, 75, 80, 85, 90]
    return make_weights(weight_entries)

@pytest.fixture
def data_dir(tmp_path):
    test_data_dir = os.path.join(tmp_path, "data")
    os.makedirs(test_data_dir, exist_ok=True)
    return test_data_dir

def test_get_change_trend_returns_float(weights):
    trend = get_change_trend(weights, 1)
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
    trend = get_change_trend(weights, 5)
    assert trend == -25

def test_get_changed_weights_since_1_day(weights):
    changed_weights = get_changed_weights_since(weights, 1)
    assert_frame_equal(changed_weights, weights[:1])

    
def test_get_changed_weights_since_3_days(weights):
    changed_weights = get_changed_weights_since(weights, 3)
    assert_frame_equal(changed_weights, weights[:3])

def test_reporting_weights_updates_the_loaded_weight_cache(data_dir):
    # Hydrate the cache
    get_saved_weights_list(data_dir)

    weight = report_weight(60, "kg", data_dir)
    weights = get_saved_weights_list(data_dir)

    print("weight", weight)
    print("weights", weights)

    assert len(weights) == 1
    assert weights[0]["weight"] == weight["weight"]
    assert weights[0]["unit"] == weight["unit"]
    assert weights[0]["timestamp"] == weight["timestamp"]
