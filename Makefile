.PHONY: micro-python deploy

# Mac
# espport=/dev/tty.usbserial-0001
# Linux
espport=/dev/ttyUSB0

# python3 -m venv .venv
# source .venv/bin/activate

install-tools:
	pip install esptool mpremote

micro-python:
	esptool.py -p ${espport} erase_flash
	esptool.py -p ${espport} write_flash -z 0x1000 images/ESP32_GENERIC-20241129-v1.24.1.bin

deploy-lib:
	mpremote connect port:${espport} fs cp -r mrequests :
	mpremote connect port:${espport} fs ls mrequests

deploy:
	mpremote connect port:${espport} fs cp *.py :
	mpremote connect port:${espport} fs cp .config.py :config.py
	mpremote connect port:${espport} fs ls

# Ctrl-X to stop
repl:
	mpremote connect port:${espport} repl

#.
