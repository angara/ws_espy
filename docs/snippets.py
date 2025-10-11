
### DS18x20

from machine import Pin
import onewire

ow = onewire.OneWire(Pin(12)) # create a OneWire bus on GPIO12
ow.scan()               # return a list of devices on the bus
ow.reset()              # reset the bus
# ow.readbyte()           # read a byte
# ow.writebyte(0x12)      # write a byte on the bus
# ow.write('123')         # write bytes on the bus
# ow.select_rom(b'12345678') # select a specific device by its ROM code

# # # # # # # # # #

import time
import ds18x20

ds = ds18x20.DS18X20(ow)
roms = ds.scan()
ds.convert_temp()
time.sleep_ms(750)
for rom in roms:
    print(ds.read_temp(rom))



# sim900

cmds = [
    "AT",             
    "AT+CFUN=1",
    'AT+SAPBR=3,1,"CONTYPE","GPRS"',
    # AT+SAPBR=3,1,"APN","your_apn",
    "AT+SAPBR=1,1",     # gprs session
    "AT+SAPBR=2,1"      # get status
]

http = [
    "at+httpinit",
    'at+HTTPPARA?',
    'AT+HTTPPARA="USERDATA","Accept: application/json"',
    'at+httppara="URL","http://rs.angara.net/meteo/_in"',
    'AT+HTTPPARA="USERDATA","Authorization: Basic dXNlcjpwYXNz\r\n"',
    'at+httpaction=0',
    'at+httpread',
    'at+httpterm'
]


ppp_dial = [
    'AT+CGDCONT=1,"IP","internet.tele2.ru"',
    'AT+CGATT=1',
    'ATD*99***1#',
# CONNECT
]


clo = [
    'at+AT+SAPBR=0,1'
]
