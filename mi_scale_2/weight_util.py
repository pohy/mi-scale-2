from datetime import datetime, timedelta
import json
import os

from mi_scale_2.config import MAX_WEIGHT, MIN_WEIGHT, DATA_DIR
from mi_scale_2.logger import log

def get_saved_weights():
    weights = []
    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json"):
            continue
        with open(f"{DATA_DIR}/{filename}", "r") as f:
            data = json.load(f)
            if data["weight"] < float(MIN_WEIGHT) or data["weight"] > float(MAX_WEIGHT):
                continue
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
            weights.append(data)

    weights.sort(key=lambda x: x["timestamp"])
    return weights

def get_changed_weights_since(date: datetime):
    weights = get_saved_weights()
    return [weight for weight in weights if weight["timestamp"] >= date]
    
def get_change_trends(days: list[int]) -> list[float]:
    weights = get_saved_weights()
    if len(weights) == 0:
        return []
    trends = []
    for day in days:
        trends.append(get_change_trend(weights, day))
    return trends

def get_change_trend(weights, days_until: int) -> float:
    weights = get_changed_weights_since(weights, datetime.now() - timedelta(days=days_until))
    log.info(f"weights since {datetime.now() - timedelta(days=days_until)}: {weights}")
    log.info(f"first weight: {weights[0]}, last weight: {weights[-1]}")
    weights = [weight["weight"] for weight in weights]
    if len(weights) == 0:
        return None
    return weights[0] - weights[-1]

def get_change_average(weights, days_until: int):
    weights = get_changed_weights_since(weights, datetime.now() - timedelta(days=days_until))
    # Sort by highest weight
    weights.sort(key=lambda x: x["weight"], reverse=True)
    # Keep only the max weight per day
    weights = {weight["timestamp"].date(): weight for weight in weights}
    # Convert from dict back to list
    weights = list(weights.values())
    # Keep only the weight value
    weights = [weight["weight"] for weight in weights]

    if len(weights) == 0:
        return None
    return sum(weights) / len(weights)

def get_changed_weights_since(weights, date: datetime):
    return [weight for weight in weights if weight["timestamp"] >= date]
