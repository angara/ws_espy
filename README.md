# ESP32 based weather station


## Wiring

- green - 485-A
- blue  - 485-B
- black - Gnd
- brown - +Vcc (10-30V)

4800 8N1 CRC

120 Ohm line terminal resistor

addr: 1

### Config

- https://devices.esphome.io/devices/Renke-RS-FSJT-N01-Wind-Speed
- https://devices.esphome.io/devices/Renke-RS-FXJT-N01-Wind-Direction

### Protocol

   
send (addr, func, reg, num, crc): 0x01  0x03  0x00 0x00  0x00 0x01  0x84 0x0A
recv (addr, func, len, bytes, crc): 0x01  0x03  0x02  0x00 0x56  0x38 0x7A

0x00 0x56 -> 86 -> 8.6 m/s


config registers: 40001, 40002

? 0100H 40101 device address (0-252) read and write
? 0101H 40102 baud rate (2400/4800/9600) read and write

? The device modbus address is stored in register 2000.

? The device baud rate is configured in register 2001 using an ID:
?
? Baud rate	ID
? 2400  0
? 4800  1
? 9600  2



mbpoll -m rtu -b 4800 -d 8 -P none -s 1 -a 1 -r 0 -c 1 -l 1000 -o 1 /dev/tty.usbserial-1340

### Links

- https://kotyara12.ru/iot/esp32_rs485_modbus/


## ESP32

- https://github.com/espressif/esptool

pip install esptool

- https://micropython.org/download/ESP32_GENERIC/
- https://micropython.org/download/SEEED_XIAO_SAMD21/


https://pypi.org/project/adafruit-ampy/

pip install adafruit-ampy

```sh
export AMPY_PORT=/dev/tty.SLAB_USBtoUART
ampy ls
```

esptool.py -p /dev/tty.usbserial-0001  erase_flash
;; -c esp32

esptool.py -p /dev/tty.usbserial-0001 -b 460800 write_flash -z 0x1000 img/ESP32_GENERIC-20240602-v1.23.0.bin
;; -b 921600


### DS18x20

```python
from machine import Pin
import onewire

ow = onewire.OneWire(Pin(12)) # create a OneWire bus on GPIO12
ow.scan()               # return a list of devices on the bus
ow.reset()              # reset the bus
# ow.readbyte()           # read a byte
# ow.writebyte(0x12)      # write a byte on the bus
# ow.write('123')         # write bytes on the bus
# ow.select_rom(b'12345678') # select a specific device by its ROM code
```

```python

import time, ds18x20
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
ds.convert_temp()
time.sleep_ms(750)
for rom in roms:
    print(ds.read_temp(rom))

```

```python

# import webrepl_setup

import machine
pin = machine.Pin(2, machine.Pin.OUT)
pin.on()
pin.off()

```


