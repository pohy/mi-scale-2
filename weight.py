import argparse
from datetime import datetime
import json
import logging
import os
import notification

from dotenv import dotenv_values

from logger import log, basicConfig
from mqttpublisher import MqttPublisher
from scanner import start

def start_weight_listener():
    config = dotenv_values(os.path.dirname(__file__) + "/.env")
    # parser = argparse.ArgumentParser(description="Get Xiaomi Mi Smart Scale 2 weight and publishing to mqtt.",
    #                                  epilog="with <3 by @qbbr")
    # parser.add_argument("--loglevel", dest="logLevel", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    #                     help="set the logging level")

    # args = parser.parse_args()
    # if args.logLevel:
    basicConfig(level=getattr(logging, 'DEBUG'))

    def callback(weight, unit):
        log.info("received data = %s %s", weight, unit)
        if weight < float(config.get("MIN_WEIGHT")) or weight > float(config.get("MAX_WEIGHT")):
            log.warning("weight is not between %s and %s, skip publishing", config.get("MIN_WEIGHT"),
                        config.get("MAX_WEIGHT"))
            return

        # publisher = MqttPublisher(config)
        # publisher.publish(weight)
        report_weight(weight, "kg")
        notification.send(weight)

    start(config.get("MAC_ADDRESS"), float(config.get("TIMEOUT")), callback)

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