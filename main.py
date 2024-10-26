

import time

from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20


# ds = ds18x20.DS18X20(ow)
# roms = ds.scan()
# ds.convert_temp()
# time.sleep_ms(750)
# for rom in roms:
#     print(ds.read_temp(rom))


# ow = onewire.OneWire(Pin(12)) # create a OneWire bus on GPIO12
# ow.scan()               # return a list of devices on the bus
# ow.reset()              # reset the bus
# ow.readbyte()           # read a byte
# ow.writebyte(0x12)      # write a byte on the bus
# ow.write('123')         # write bytes on the bus
# ow.select_rom(b'12345678') # select a specific device by its ROM code

DS1820_PIN = 14

def read_temp(pin_id):
  ds = DS18X20(OneWire(Pin(pin_id)))
  roms = ds.scan()
  print(f'pin:{pin_id} {roms=}')
  if roms:
    ds.convert_temp()
    time.sleep_ms(750)
    return ds.read_temp(roms[0])


print("t:", read_temp(DS1820_PIN))
