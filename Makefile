.PHONY: micro-python deploy deploy-lib repl install-tools

# Mac
# espport=/dev/tty.usbserial-0001
# Linux
espport=/dev/ttyUSB0


install:
	uv venv
	uv pip install esptool mpremote
	@echo "to activate venv run: source .venv/bin/activate"

#	python3 -m venv .venv
#	pip install esptool mpremote 
#   pip install micropython-esp32-stubs # VSCode support

flash-micropython:
	esptool.py -p ${espport} erase_flash
	esptool.py -p ${espport} write_flash -z 0x1000 images/ESP32_GENERIC-20241129-v1.24.1.bin
	sleep 1

deploy-lib:
	mpremote connect port:${espport} fs cp -r mrequests :
	mpremote connect port:${espport} fs ls mrequests

deploy:
	mpremote connect port:${espport} fs cp *.py :
	mpremote connect port:${espport} fs cp .config.py :config.py
	mpremote connect port:${espport} fs ls


init-board: flash-micropython deploy-lib deploy

# Ctrl-X to stop, Ctrl-D to restart
repl:
	mpremote connect port:${espport} repl

#.
