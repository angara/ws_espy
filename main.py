
VERSION = "ws_esp 2024.11.01"

import time

from collections import Counter

from machine import Pin, UART
from onewire import OneWire
from ds18x20 import DS18X20

import config
import conn


# pins:
#
Uart2 = UART(2, 4800)  # RX2 = 16, TX2 = 17
DsPin = Pin(15)
Led   = Pin(2, Pin.OUT)

def read_temp():
  ds = DS18X20(OneWire(DsPin))
  roms = ds.scan()
  print(f'read_temp:{DsPin} {roms=}')
  if roms:
    ds.convert_temp()
    time.sleep_ms(750)
    return ds.read_temp(roms[0])
  else:
    print("read_temp:{DsPin} no ds18b20 found")
    return None
#

POLL1 = b'\x01\x03\x00\x00\x00\x01\x84\x0A'

RESP = b'\x01\x03\x02\x00\x56\x38\x7A'

# 0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A
# 0x01 0x03 0x02 0x00 0x56 0x38 0x7A

def uart_send_recv(data:bytes) -> bytes:
  # uart = UART(2, BAUD2)
  # print(f'{uart=}')
  # dere = Pin(DE2, Pin.OUT)
  # uart.init(baudrate=SPEED2, bits=8, parity=None, stop=1, 
  #           rx=RX2, tx=TX2, rts=RTS2,
  #           timeout=1000, timeout_char=1000,
  #           )
  # time.sleep_us(FRAME_GAP_US)
  # dere.on()
  Led.on()
  # rc = uart.write(data)
  # print('write.rc:', rc)
  # rc = uart.flush()
  # print('flush.rc:', rc)
  # time.sleep_us(FRAME_GAP_US)
  time.sleep_ms(100)

  # dere.off()
  # led.off()
  #resp = uart.read()
  # print(">", uart.any())
  for i in range(100):
    print(Uart2.read())
    print(Uart2.write(RESP))
    # while uart.any():
    #   b = uart.read(1)
    #   print(f'{b=}')
    # print(i)
    time.sleep(1)

  Led.off()
  # print('resp:', resp)
  # return resp



# def wind():
#   Led.on()
#   print("write.n:", uart.write(POLL1))
#   resp = uart.read()
#   print(f'{resp=}')
#   return resp


WIND_READ_COUNT = 10
WIND_READ_DELAY = 5

LOOP_DELAY = 10


# # # # #


def read_wind():
  Led.on()
  time.sleep(1)
  Led.off()
  return 2
#

def read_rhumb():
  Led.on()
  time.sleep(1)
  Led.off()
  return 1
#

# # # # #

WIND_MINIMAL = 0.8

RHUMBS = [0, 45, 90, 135, 180, 225, 270, 315]

def process_wind(wind_data):
  """returns dict(w=, g=, b=)"""
  res = {}
  rhs = [b for w,b in wind_data if (w is not None) and (w >= WIND_MINIMAL) and (b is not None)]
  rhs = Counter(rhs).most_common()
  print("process_wind: rhubms moust_common:", rhs) ###
  if rhs:
    r = rhs[0][0]
    if r >= 0 and r < len(RHUMBS):
      res['b'] = RHUMBS[r]
    else:
      print("process_wind: unexpected rhumb value", rhs)
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
  print(time.time())
  wind_data = [(read_wind(), read_rhumb(),) 
               for _ in range(WIND_READ_COUNT) if not time.sleep(WIND_READ_DELAY)]
  print(f'{wind_data}')
  res = process_wind(wind_data)
  #
  temp = read_temp()
  print(f'{temp}')
  if temp is not None:
    res['t'] = temp
  #
  attempt_count += 1
  if hwid := conn.setup_wifi(config.WIFI_SSID, config.WIFI_PASS):
    res['hwid'] = config.HWID or hwid
    rc = conn.submit_data(config.SUBMIT_URL, config.AUTH_BASIC, res)
    print("send_data() response:", rc)
    # TODO: if rc.ok clear error_count
  else:
    print("wifi setup failed")
  #
  # if attempt_count > ATTEMPT_MAX:
  #  reboot
  time.sleep(LOOP_DELAY)
#

# # # # #

if __name__ == '__main__':
  setup()
  while True:
    try:
      loop()
    except Exception as ex:
      print("main loop except:", ex)
    time.sleep(1)
#.
