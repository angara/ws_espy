
# Mac
# espport=/dev/tty.usbserial-0001
# espport=/dev/tty.usbmodem14601

ENV_FILE ?= .env

# generic ESP32
espport=/dev/ttyUSB0
python_image=images/ESP32_GENERIC-20250911-v1.26.1.bin

# ESP32-C3
# espport=/dev/ttyACM0
# python_image=images/ESP32_GENERIC_C3-20241129-v1.24.1.bin


install:
	uv venv
	uv add esptool mpremote micropython-esp32-stubs
	@echo "to activate venv run: source .venv/bin/activate"

flash-micropython:
	uv run esptool -p ${espport} erase-flash
	uv run esptool -p ${espport} write-flash -z 0x1000 ${python_image}
	sleep 1

flash-micropython-c3:
	esptool.py -p ${espport} erase_flash
	esptool.py -p ${espport} write_flash 0 ${python_image}
	sleep 1

deploy-libs:
	uv run mpremote connect port:${espport} fs cp -r mrequests :
	uv run mpremote connect port:${espport} fs ls mrequests

deploy-code:
	uv run mpremote connect port:${espport} fs cp *.py :

deploy-config:
	uv run mpremote connect port:${espport} fs cp ${ENV_FILE} :.env

# dev:
# 	uv run mpremote connect port:${espport} fs cp *.py :
# 	uv run mpremote connect port:${espport} repl

init-board: flash-micropython deploy-lib deploy

init-board-c3: flash-micropython-c3 deploy-lib deploy

# Ctrl-X to stop, Ctrl-D to restart
repl:
	uv run mpremote connect port:${espport} repl


.PHONY: dev repl install flash-micro-python deploy-libs deploy-code
