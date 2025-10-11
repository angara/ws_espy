.PHONY: micro-python deploy deploy-lib repl install-tools

# Mac
# espport=/dev/tty.usbserial-0001
# espport=/dev/tty.usbmodem14601

# generic ESP32
espport=/dev/ttyUSB0
# python_image=images/ESP32_GENERIC-20241129-v1.24.1.bin
python_image=images/ESP32_GENERIC-20250809-v1.26.0.bin

# ESP32-C3
# espport=/dev/ttyACM0
# python_image=images/ESP32_GENERIC_C3-20241129-v1.24.1.bin


install:
	uv venv
	uv add esptool mpremote micropython-esp32-stubs
	@echo "to activate venv run: source .venv/bin/activate"

flash-micropython:
	uv run esptool -p ${espport} erase_flash
	uv run esptool -p ${espport} write_flash -z 0x1000 ${python_image}
	sleep 1

flash-micropython-c3:
	esptool.py -p ${espport} erase_flash
	esptool.py -p ${espport} write_flash 0 ${python_image}
	sleep 1

deploy-lib:
	mpremote connect port:${espport} fs cp -r mrequests :
	mpremote connect port:${espport} fs ls mrequests

deploy:
	mpremote connect port:${espport} fs cp *.py :
	mpremote connect port:${espport} fs cp .config.py :config.py
	mpremote connect port:${espport} fs ls

dev:
	uv run mpremote connect port:${espport} fs cp gprs.py :
	uv run mpremote connect port:${espport} repl

init-board: flash-micropython deploy-lib deploy

init-board-c3: flash-micropython-c3 deploy-lib deploy

# Ctrl-X to stop, Ctrl-D to restart
repl:
	uv run mpremote connect port:${espport} repl

#.
