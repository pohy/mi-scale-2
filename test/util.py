from datetime import datetime, timedelta

def make_weights(entries: list[float]):
    return [{
        "weight": float(entry),
        "timestamp": (datetime.now() - timedelta(days=i)),
        "unit": "kg"
    } for i, entry in enumerate(entries)]
