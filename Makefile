

espport=/dev/tty.usbserial-0001
# espbaud=460800
espbaud=115200
esptool=esptool.py
rshell=rshell

# pip install esptool
# pip install adafruit-ampy

micro-python:
	${esptool} -p ${espport} -b ${espbaud} erase_flash
# -c esp32

	${esptool} -p ${espport} -b ${espbaud} write_flash -z 0x1000 images/ESP32_GENERIC-20240602-v1.23.0.bin
# -b 921600

deploy:
	${rshell} -b ${espbaud} -p ${espport} --timing cp *.py /pyboard/

# Ctrl-X to stop
repl:
	${rshell} -b ${espbaud} -p ${espport} repl


.PHONY: micro-python deploy