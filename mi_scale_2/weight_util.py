import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from mi_scale_2.config import MAX_WEIGHT, MIN_WEIGHT, DATA_DIR
from mi_scale_2.logger import log

last_loaded_at = None
last_loaded_weights = None
last_loaded_ttl_s = 60
def get_saved_weights_list():
    global last_loaded_at, last_loaded_weights
    if last_loaded_at is not None and (datetime.now() - last_loaded_at).total_seconds() < last_loaded_ttl_s:
        return last_loaded_weights
    weights = []
    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json"):
            continue
        with open(f"{DATA_DIR}/{filename}", "r") as f:
            data = json.load(f)
            weights.append(data)

    weights.sort(key=lambda x: x["timestamp"])

    last_loaded_at = datetime.now()
    last_loaded_weights = weights

    return weights


def report_weight(weight: float, unit: str):
    """Saves weight to file in JSON format
    Name of the file is current date and time (e.g. 2020-01-01_00-00-00.json)

    Example:
        {
            "weight": 80.0,
            "unit": "kg",
            "timestamp": "2020-01-01T00:00:00.000000Z"
        }
    """
    data = {
        "weight": weight,
        "unit": unit,
        "timestamp": datetime.now().isoformat()
    }
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    with open(path.join(DATA_DIR, filename), "w") as f:
        json.dump(data, f)
    last_loaded_weights.append(data)

def get_change_trends(days: list[int]) -> list[float]:
    weights = get_saved_weights()
    if len(weights) == 0:
        return []
    trends = []
    for day in days:
        trends.append(get_change_trend(weights, day))
    return trends

def get_change_trend(_weights, days_until: int) -> float:
    weights = _weights.copy()
    weights = weights[weights["days"] <= days_until]
    if len(weights) == 0:
        return None
    return weights["delta"].iat[-1]

def get_changed_weights_since(weights, days_until: int):
    return weights[weights["days"] <= days_until - 1]

def keep_only_daily_highest_weight(_weights):
    # Sort by highest weight
    weights = _weights.copy()
    weights = weights.sort_values(by="weight")
    weights = weights.drop_duplicates("days", keep="last")
    weights = weights.sort_values(by="timestamp")
    return weights

def get_saved_weights():
    df = pd.DataFrame(get_saved_weights_list())#.apply(lambda data: datetime.fromisoformat(data["timestamp"]))
    return process_raw_weights(df)

def process_raw_weights(_df: pd.DataFrame) -> pd.DataFrame:
    df = _df.copy()
    df["weight"] = df["weight"].fillna(-1).astype(float)
    # Filter out weights outside the configured range
    df = df[(df['weight'] >= MIN_WEIGHT) & (df['weight'] <= MAX_WEIGHT)]

    df["timestamp"] = df["timestamp"].astype("datetime64[ms]")
    df["dt"] = df["timestamp"].astype("datetime64[ms]")
    df = df.sort_values(by="dt", ascending=False).drop(columns=["unit"])

    df["days"] = df["dt"].rsub(pd.Timestamp('today')).dt.days
    df["weeks"] = np.floor(df["days"] / 7).astype(int)

    print("first row", df.iloc[0], "last row", df.iloc[-1])
    df["delta"] = df["weight"].rsub(df["weight"].iloc[0])
    df["trend"] = df["delta"].apply(lambda delta: "Gain" if delta > 0 else "Loss")

    return df


def get_weights_for(weights, drop_by = 'all'):
    weights = weights.copy()
    weights = weights.sort_values(by="weight", ascending=False)

    if drop_by in ['days', 'weeks']:
        weights = weights.drop_duplicates(drop_by)

    return weights.sort_values(by="days")
