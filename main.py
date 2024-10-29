

import time

from machine import Pin, UART
from onewire import OneWire
from ds18x20 import DS18X20


led = Pin(2, Pin.OUT)

DS1820_PIN = 15

RX2 = 16
TX2 = 17
DE2 = 18
BAUD2 = 4800


dere = Pin(DE2, Pin.OUT)
uart = UART(2, BAUD2)

# 3.5 chars between frames, 1.5 between bytes, not less that 1.75
FRAME_GAP_US = int(1750 if BAUD2 > 19200 else (3.5*11*1000000 / BAUD2))

print('frame_gap_us:', FRAME_GAP_US)

def read_temp(pin_id):
  ds = DS18X20(OneWire(Pin(pin_id)))
  roms = ds.scan()
  print(f'pin:{pin_id} {roms=}')
  if roms:
    ds.convert_temp()
    time.sleep_ms(750)
    return ds.read_temp(roms[0])
  else:
    print("read_temp: no ds18b20 found")
    return None


print("t:", read_temp(DS1820_PIN))

POLL1 = b'\x01\x03\x00\x00\x00\x01\x84\x0A'

RESP = b'\x01\x03\x02\x00\x56\x38\x7A'

# 0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A
# 0x01 0x03 0x02 0x00 0x56 0x38 0x7A

def uart_send_recv(data:bytes) -> bytes:
  # uart = UART(2, BAUD2)
  print(f'{uart=}')
  # dere = Pin(DE2, Pin.OUT)
  # uart.init(baudrate=SPEED2, bits=8, parity=None, stop=1, 
  #           rx=RX2, tx=TX2, rts=RTS2,
  #           timeout=1000, timeout_char=1000,
  #           )
  time.sleep_us(FRAME_GAP_US)
  # dere.on()
  led.on()
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
    print(uart.read())
    print(uart.write(RESP))
    # while uart.any():
    #   b = uart.read(1)
    #   print(f'{b=}')
    # print(i)
    time.sleep(1)

  led.off()
  # print('resp:', resp)
  # return resp


# while uart0.any() > 0:
#     rxData += uart0.read(1)


def test1():
  uart_send_recv(POLL1)


def wind():
  led.on()
  print("write.n:", uart.write(POLL1))
  resp = uart.read()
  print(f'{resp=}')
  return resp

wind()
