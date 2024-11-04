
VERSION = "ws_esp 2024.11.04"

import time

from machine import Pin, UART, reset
from onewire import OneWire
from ds18x20 import DS18X20

import config
import conn
import modbus

# pins:
#
Uart2 = UART(2, 4800)  # RX2 = 16, TX2 = 17
DsPin = Pin(15)
Led   = Pin(2, Pin.OUT)


def blink(n:int):
  D = 0.5 if n < 5 else 0.3
  Led.off()
  time.sleep(0.5)
  for _ in range(n):
    time.sleep(D)
    Led.on()
    time.sleep(D)
    Led.off()
  time.sleep(0.5)
#

# # # # #

def read_temp():
  ds = DS18X20(OneWire(DsPin))
  roms = ds.scan()
  print(f'read_temp({DsPin}): {roms=}')
  if roms:
    ds.convert_temp()
    time.sleep_ms(750)
    return ds.read_temp(roms[0])
  else:
    print(f"read_temp({DsPin}): no ds18b20 found!")
    return None
#

def read_wind():
  Led.on()
  w10 = modbus.read_register(Uart2, 1, 0)
  Led.off()
  return w10 / 10 if w10 is not None else None
#

def read_rhumb():
  Led.on()
  rh = modbus.read_register(Uart2, 2, 0)
  Led.off()
  return rh
#

# # # # #

WIND_READ_COUNT = 10
WIND_READ_DELAY = 5

LOOP_DELAY = 10
ATTEMPT_MAX = 10

WIND_MINIMAL = 0.8
RHUMBS = [0, 45, 90, 135, 180, 225, 270, 315]

def main_rhumb_degree(rhs):
  """return main rhumb degree value or None"""
  try:
    res = [0 for _ in range(len(RHUMBS))]
    for r in rhs:
      if r >= 0 and r < len(res):
        res[r] += 1
    if m := max(res):
      return RHUMBS[res.index(m)]
  except Exception as ex:
    print(f'main_rhumb_degree exception: {rhs=}', ex)
  return None


def process_wind(wind_data):
  """returns dict(w=, g=, b=)"""
  res = {}
  rhs = [b for w,b in wind_data if (w is not None) and (w >= WIND_MINIMAL) and (b is not None)]
  print(f"process_wind: {rhs=}") ###
  b = main_rhumb_degree(rhs)
  if b is not None:
    res['b'] = b
  #
  ms = [w for w,_ in wind_data if w is not None]
  if ms:
    res['w'] = sum(ms) / len(ms)
    res['g'] = max(ms)
  #
  return res
#

# # # # #

def setup():
  print(VERSION)
  print(f'{DsPin=}')
  print(f'{Uart2=}')
#

attempt_count = 0

def loop():
  global attempt_count

  print("uptime:", time.time())
  wind_data = [(read_wind(), read_rhumb())
               for _ in range(WIND_READ_COUNT) if not time.sleep(WIND_READ_DELAY)]
  print(f'{wind_data=}') ###
  req = process_wind(wind_data)
  #
  Led.on()
  temp = read_temp()
  Led.off()
  print(f'{temp=}')
  if temp is not None:
    req['t'] = temp
  #
  attempt_count += 1
  if hwid := conn.setup_wifi(config.WIFI_SSID, config.WIFI_PASS):
    req['hwid'] = config.HWID or hwid
    req['uptime'] = time.time()
    rc = conn.submit_data(config.SUBMIT_URL, (config.SUBMIT_USER, config.SUBMIT_PASS), req)
    # print("send_data() response:", rc.status_code, rc.text)
    print("send_data() response:", rc)  ###
    if rc.status_code == 200:
      attempt_count = 0
      blink(2)
    else:
      blink(4)
  else:
    print("wifi setup failed!")
  #
  if attempt_count > ATTEMPT_MAX:
    print("too many failed attempts! reset...")
    reset()
  #
  time.sleep(LOOP_DELAY)
#

# # # # #

def main():
  setup()
  while True:
    try:
      loop()
    except Exception as ex:
      print("main loop except:", ex)
      blink(6)
    time.sleep(1)
#
