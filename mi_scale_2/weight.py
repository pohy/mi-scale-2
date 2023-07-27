from os import path
from datetime import datetime
import json
import logging

from mi_scale_2.notification import send_notification
from mi_scale_2.config import MAC_ADDRESS, TIMEOUT, MIN_WEIGHT, MAX_WEIGHT, DATA_DIR
from mi_scale_2.logger import log, basicConfig
from mi_scale_2.scanner import start_scanning
from mi_scale_2.weight_util import report_weight

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
