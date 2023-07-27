from pandas import DataFrame
from datetime import datetime, timedelta
from mi_scale_2.weight_util import process_raw_weights

def make_weights(entries: list[float]):
    weights = [{
        "weight": float(entry),
        "timestamp": (datetime.now() - timedelta(days=i)),
        "unit": "kg"
    } for i, entry in enumerate(entries)]
    return process_raw_weights(DataFrame(weights))
