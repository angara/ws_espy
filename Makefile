

espport=/dev/tty.usbserial-0001
# espbaud=460800
espbaud=115200
esptool=esptool.py

# pip install esptool
# pip install mpremote
# pip install adafruit-ampy

micro-python:
	${esptool} -p ${espport} -b ${espbaud} erase_flash
# -c esp32

	${esptool} -p ${espport} -b ${espbaud} write_flash -z 0x1000 images/ESP32_GENERIC-20240602-v1.23.0.bin
# -b 921600

deploy-lib:
#	ampy --port ${espport} put mrequests /mrequests
	mpremote connect port:${espport} fs cp -r mrequests :
	mpremote connect port:${espport} fs ls mrequests

deploy:
# ampy --port ${espport} put boot.py
# ampy --port ${espport} put conn.py
# ampy --port ${espport} put config.py
# ampy --port ${espport} put modbus.py
# ampy --port ${espport} put main.py
# ampy --port ${espport} ls
	mpremote connect port:${espport} fs cp *.py :
	mpremote connect port:${espport} fs ls

# Ctrl-X to stop
repl:
	mpremote connect port:${espport} repl


.PHONY: micro-python deploy