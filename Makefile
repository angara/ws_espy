.PHONY: micro-python deploy

espport=/dev/tty.usbserial-0001
# espbaud=460800
espbaud=115200


install-tools:
	pip install esptool mpremote

micro-python:
	esptool.py -p ${espport} -b ${espbaud} erase_flash
	esptool.py -p ${espport} -b ${espbaud} write_flash -z 0x1000 images/ESP32_GENERIC-20240602-v1.23.0.bin

deploy-lib:
	mpremote connect port:${espport} fs cp -r mrequests :
	mpremote connect port:${espport} fs ls mrequests

deploy:
	mpremote connect port:${espport} fs cp *.py :
	mpremote connect port:${espport} fs ls

# Ctrl-X to stop
repl:
	mpremote connect port:${espport} repl

#.
