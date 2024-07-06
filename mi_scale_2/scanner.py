import time
from bluepy.btle import Scanner, DefaultDelegate

from mi_scale_2.config import SCAN_FREQUENCY_HZ
from mi_scale_2.logger import log

scan_frequency_sec = 1/SCAN_FREQUENCY_HZ


class ScanDelegate(DefaultDelegate):
    # 1 - flags, 2 - Incomplete 16b Services, 255 - Manufacturer, 22 - 16b Service Data, 9 - Complete Local Name
    SERVICE_DATA = 22  # [1d18828809e4070310112302]

    def __init__(self, mac_address, callback):
        DefaultDelegate.__init__(self)
        self.mac_address = mac_address.upper()
        self.last_raw_data = None
        self.callback = callback

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if self.mac_address == dev.addr.upper():
            self.parse_data(dev)

    def parse_data(self, dev):
        # log.debug("device %s is %s, rssi: %d dBm, connectable: %s",
                #   dev.addr, dev.addrType, dev.rssi, dev.connectable)

        for (tag, desc, value) in dev.getScanData():
            if tag == self.SERVICE_DATA and value.startswith("1d18"):
                raw_data = bytes.fromhex(value[4:])
                # log.debug(f'raw_data: {raw_data}')
                if raw_data == self.last_raw_data:
                    # log.debug("skip duplicate data")
                    return

                is_stabilized = (raw_data[0] & (1 << 5)) != 0
                is_weight_removed = (raw_data[0] & (1 << 7)) != 0
                self.last_raw_data = raw_data

                if is_stabilized is True and is_weight_removed is False:
                    weight = int.from_bytes(raw_data[1:3], byteorder="little") / 100

                    if (raw_data[0] & (1 << 4)) != 0:  # chinese catty
                        unit = "jin"
                    elif (raw_data[0] & (1 << 2)) != 0:  # pound
                        unit = "lbs"
                    elif (raw_data[0] & (1 << 1)) != 0:  # kg
                        unit = "kg"
                        weight /= 2  # catty to kg
                    else:
                        unit = "unknown"

                    self.callback(weight, unit)


def start_scanning(mac_address, timeout, callback):
    log.info("scanner is starting...")
    scanner = Scanner().withDelegate(ScanDelegate(mac_address, callback))

    set_interval(lambda: tick(scanner, timeout), scan_frequency_sec)
    # while True:
    #     tick(scanner, timeout)

def time_now_ms():
    return int(round(time.time() * 1000))

last_tick = time_now_ms()
notified = False
def tick(scanner: Scanner, timeout: int):
    global last_tick
    global notified

    if not notified:
        log.info('First scan!')
        notified = True

    log.debug(f"scanner is processing... since last_tick: {time_now_ms() - last_tick}ms")

    scanner.start()
    scanner.process(timeout)
    scanner.stop()

    last_tick = time_now_ms()

import threading

def set_interval(func, sec):
    def func_wrapper():
        func()
        set_interval(func, sec)
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
