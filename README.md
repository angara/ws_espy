# ESP32 based weather station

```ws_espy 2025.11.04```


## Dev seteup

- `python`
- `uv`
- `make`


## Wind sensor wiring

PR-3000-FSJT-N01

- green - 485-A
- blue  - 485-B
- black - Gnd
- brown - +Vcc (10-30V)

4800 8N1 CRC

120 Ohm line terminal resistor

addr: 1

- https://devices.esphome.io/devices/Renke-RS-FSJT-N01-Wind-Speed
- https://devices.esphome.io/devices/Renke-RS-FXJT-N01-Wind-Direction

### Module connection cable

- orange       - +5
- orange-white - not connected
- green        - 1-wire data
- green-white  - ground

- brown        - +12
- brown-white  - ground
- blue         - 485-B
- blue-white   - 485-A

### Modbus notes

Sample:

- send (addr, func, reg, num, crc): 0x01  0x03  0x00 0x00  0x00 0x01  0x84 0x0A
- recv (addr, func, len, bytes, crc): 0x01  0x03  0x02  0x00 0x56  0x38 0x7A
- value: 0x00 0x56 -> 86 -> 8.6 m/s

- The device modbus address is stored in register 2000 (0x07D0) - [1-247] 
- The device baud rate is configured in register 2001 using an ID:

- ? Baud rate ID
- ? 2400  0
- ? 4800  1
- ? 9600  2
- ? 19200 3

RHUMBS = [0, 45, 90, 135, 180, 225, 270, 315]


```sh
mbpoll -m rtu -b 4800 -d 8 -P none -s 1 -a 1 -r 1 -c 1 -l 1000 -o 1 /dev/tty.usbserial-1340
```

- https://kotyara12.ru/iot/esp32_rs485_modbus/
- https://minimalmodbus.readthedocs.io/en/stable/
- https://pymodbus.readthedocs.io/en/latest/ ???


## ESP32

MicroPython images:

- https://micropython.org/download/ESP32_GENERIC/
- https://micropython.org/download/SEEED_XIAO_SAMD21/

- https://lastminuteengineers.com/esp32-pinout-reference/
- https://lastminuteengineers.com/esp32-wroom-32-pinout-reference/
- https://github.com/espressif/esptool
- https://docs.micropython.org/en/latest/reference/mpremote.html


### Other tools

- https://github.com/astral-sh/uv
- https://docs.astral.sh/uv/

- https://pypi.org/project/adafruit-ampy/
- https://github.com/dhylands/rshell
- https://github.com/wendlers/mpfshell


## Application

### Libraries

Copy files from repo to `mrequests` folder:

- https://github.com/SpotlightKid/mrequests

### Config environment

Copy `env.example` to `.env` and set correct values.

Use `ENV_FILE` to specify different config file.

```sh
ENV_FILE=.env make deploy-config
```


### Set Device Address

```apt install python3-serial```

See:
```scripts/setaddr.py```

```
read_register(addr=1,2000) 01030200017984
1
read_register(addr=1,2001) 01030200017984
1
read_register(addr=1,2002) 0103020000b844
0
read_register(addr=1,2003) 01030266ed53a9
26349
read_register(addr=1,2004) 0103024d5e0cec
19806
```


## ESP32 C3 Super Mini

- <https://www.espboards.dev/esp32/esp32-c3-super-mini/>

- Blue LED (gpio 8)


## TODO

- implement interactive configuration
