from machine import UART, Pin
import time

# uart = UART(2, tx=17, rx=16, baudrate=115200)

# uart = UART(2, 9600)

# uart.write("AT\r\n")
# time.sleep(1)
# print(uart.read())


# uart = UART(1, tx=Pin(22), rx=Pin(23))


MODEM_TX  = 12  # D2
MODEM_RX  = 14  # D3
MODEM_PWR = 13  # D9


modem = UART(1, 9600, tx=MODEM_TX, rx=MODEM_RX)


def send_at(cmd:str, timeout=2000, end=b'\r\n') -> bytes:

    while modem.any():
        modem.read()

    modem.write(cmd.encode() + end)

    start = time.ticks_ms()
    buffer = b''

    while time.ticks_diff(time.ticks_ms(), start) < timeout:
        if umodem.any():
            buffer += modem.read()

            # if b'OK' in buffer or b'ERROR' in buffer:
            #     break
        else:
            time.sleep_ms(10)

    return buffer

# print("Response:", resp.decode(errors="ignore"))
