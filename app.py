
import time

from machine import Pin, UART, reset, unique_id
from onewire import OneWire
from ds18x20 import DS18X20

import config
import conn
import modbus


# pins:
#
if config.BOARD == "esp32-c3":
    Uart = UART(1, baudrate=115200, tx=Pin(10), rx=Pin(9))
else:
    Uart = UART(2, 4800)  # RX2 = 16, TX2 = 17

DsPin = Pin(15)
Led = Pin(2, Pin.OUT)


def blink(n: int):
    D = 0.5 if n < 5 else 0.3
    Led.off()
    time.sleep(0.5)
    for _ in range(n):
        time.sleep(D)
        Led.on()
        time.sleep(D)
        Led.off()
    time.sleep(0.5)


# def mcu_temp():
#   return (esp32.raw_temperature() - 32) * 5 / 9

# # # # #


def read_temp():
    ds = DS18X20(OneWire(DsPin))
    roms = ds.scan()
    print(f"read_temp({DsPin}): {roms=}")
    if roms:
        ds.convert_temp()
        time.sleep_ms(750) # type: ignore[unresolved-attribute]
        return ds.read_temp(roms[0])
    else:
        print(f"read_temp({DsPin}): no ds18b20 found!")
        return None


def read_wind_speed() -> float | None:
    Led.on()
    w10 = modbus.read_register(Uart, 1, 0)
    Led.off()
    return w10 / 10 if w10 is not None else None


def read_wind_dir() -> int | None:
    Led.on()
    d10 = modbus.read_register(Uart, 2, 0)
    Led.off()
    return int(d10 / 10) if d10 is not None else None


# # # # #

WIND_READ_COUNT = 100
WIND_READ_DELAY = 4
LOOP_DELAY = 1

ATTEMPT_MAX = 5

WIND_MINIMAL = 0.8


def main_dir_degrees(dirs):
    """return main direction degrees value or None"""
    try:
        histogram = [0 for _ in range(360)]
        for d in dirs:
            if d >= 0 and d < len(histogram):
                histogram[d] += 1
        if m := max(histogram):
            return histogram.index(m)
    except Exception as ex:
        print(f"main_dir_degrees exception: {dirs=}", ex)
    return None


def process_wind(wind_data: list) -> dict:
    """returns dict(w=, g=, b=)"""
    res = {}
    dirs = [
        b
        for w, b in wind_data
        if (w is not None) and (w >= WIND_MINIMAL) and (b is not None)
    ]
    print(f"process_wind: {dirs=}")  ###
    b = main_dir_degrees(dirs)
    if b is not None:
        res["b"] = b
    #
    ms = [w for w, _ in wind_data if w is not None]
    if ms:
        res["w"] = sum(ms) / len(ms)
        res["g"] = max(ms)
    #
    return res


# # # # #

hwid = config.HWID or unique_id().hex()
attempt_count = 0


def setup():
    print(f"{config.VERSION} {hwid=}")
    if config.READ_WIND:
        print(f"Wind: {Uart}")
    if config.READ_TEMP:
        print("Temp:", read_temp())


def loop():
    global attempt_count

    print("uptime:", time.time())

    if config.READ_WIND:
        wind_data = [
            (read_wind_speed(), read_wind_dir())
            for _ in range(WIND_READ_COUNT)
            if not time.sleep(WIND_READ_DELAY)
        ]
        print(f"{wind_data=}")  ###
        req = process_wind(wind_data)
    else:
        for _ in range(WIND_READ_COUNT):
            Led.on()
            time.sleep(0.004)
            Led.off()
            time.sleep(WIND_READ_DELAY)
        req = {}
    #

    if config.READ_TEMP:
        Led.on()
        temp = read_temp()
        Led.off()
        print(f"{temp=}")
        if temp is not None:
            req["t"] = temp
    #

    attempt_count += 1


    if conn.setup_wifi(config.WIFI_SSID, config.WIFI_PASS):
        req["hwid"] = hwid
        req["uptime"] = time.time()
        # req['tmcu'] = mcu_temp()
        rc = conn.submit_data(
            config.SUBMIT_URL, (config.SUBMIT_USER, config.SUBMIT_PASS), req
        )
        print("send_data() response:", rc.status_code, rc.text)
        if rc.status_code == 200:
            attempt_count = 0
            blink(2)
        else:
            blink(4)
    else:
        print("wifi setup failed!")
    #
    time.sleep(LOOP_DELAY)


# # # # #


def main():
    setup()
    while True:
        try:
            loop()
        except Exception as ex:
            print("main loop exception:", ex)
            blink(6)
        time.sleep(1)
        if attempt_count > ATTEMPT_MAX:
            print("too many failed attempts! reset...")
            reset()
        #
