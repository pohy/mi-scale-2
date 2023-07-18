from datetime import datetime, timedelta
import json
import os

from config import MAX_WEIGHT, MIN_WEIGHT


def get_weights():
    weights = []
    for filename in os.listdir("./data"):
        if not filename.endswith(".json"):
            continue
        with open("./data/" + filename) as f:
            data = json.load(f)
            if data["weight"] < float(MIN_WEIGHT) or data["weight"] > float(MAX_WEIGHT):
                continue
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
            weights.append(data)

    weights.sort(key=lambda x: x["timestamp"])
    return weights

def get_changed_weights_since(date: datetime):
    weights = get_weights()
    return [weight for weight in weights if weight["timestamp"] >= date]
    
def get_change_trends(days: list[int]) -> list[float]:
    weights = get_weights()
    if len(weights) == 0:
        return []
    trends = []
    for day in days:
        trend = get_change_trend(weights, day)
        trends.append(f"{day} days: {trend}")
    return trends

def get_change_trend(weights, days_until: int):
    weights = get_changed_weights_since(datetime.now() - timedelta(days=days_until))
    weights = [weight["weight"] for weight in weights]
    if len(weights) == 0:
        return None
    return weights[0] - weights[-1]

def get_change_average(weights, days_until: int):
    weights = get_changed_weights_since(datetime.now() - timedelta(days=days_until))
    weights = [weight["weight"] for weight in weights]
    if len(weights) == 0:
        return None
    return sum(weights) / len(weights)

def get_changed_weights_since(date: datetime):
    weights = get_weights()
    return [weight for weight in weights if weight["timestamp"] >= date]