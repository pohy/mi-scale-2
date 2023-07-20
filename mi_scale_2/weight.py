from datetime import datetime
import json
import logging

from mi_scale_2.notification import send_notification
from mi_scale_2.config import MAC_ADDRESS, TIMEOUT, MIN_WEIGHT, MAX_WEIGHT
from mi_scale_2.logger import log, basicConfig
from mi_scale_2.scanner import start_scanning

def start_weight_listener():
    basicConfig(level=getattr(logging, 'DEBUG'))

    def callback(weight, unit):
        log.info("received data = %s %s", weight, unit)
        send_notification(weight)
        if weight < float(MIN_WEIGHT) or weight > float(MAX_WEIGHT):
            log.warning("weight is not between %s and %s, skip publishing", MIN_WEIGHT,
                        MAX_WEIGHT)
            return

        report_weight(weight, "kg")

    start_scanning(MAC_ADDRESS, float(TIMEOUT), callback)

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
    with open("./data/" + filename, "w") as f:
        json.dump(data, f)
