import logging
from mi_scale_2.logger import basicConfig, log
from mi_scale_2.config import LOG_LEVEL

basicConfig(level=getattr(logging, LOG_LEVEL))

from datetime import datetime

from mi_scale_2.transports.sheet import SheetTransport
from mi_scale_2.transports.weight_transport import WeightTransport
from mi_scale_2.weight import start_weight_listener

transports: list[WeightTransport] = [
    SheetTransport(),
]

def on_measurement(weight: float, unit: str, date: datetime):
    log.info("on_measurement: %s %s at %s", weight, unit, date)
    for transport in transports:
        try:
            transport.on_measurement(weight, unit, date)
        except Exception as e:
            log.error("Failed to publish weight to %s: %s", transport, e)


if __name__ == "__main__":
    log.info('Starting weight listener...')
    start_weight_listener(on_measurement)
