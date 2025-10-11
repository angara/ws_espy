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
MODEM_PWR = 13  # D8


modem = UART(1, 9600, tx=MODEM_TX, rx=MODEM_RX)



def send_at(cmd:str, timeout=2000, end=b'\r\n') -> bytes:

    while modem.any():
        modem.read()

    modem.write(cmd.encode() + end)

    start = time.ticks_ms()
    buffer = b''

    while time.ticks_diff(time.ticks_ms(), start) < timeout:
        if modem.any():
            buffer += modem.read()

            # if b'OK' in buffer or b'ERROR' in buffer:
            #     break
        else:
            time.sleep_ms(10)

    return buffer

# print("Response:", resp.decode("ignore"))


def send_cmds(cmds, timeout=2000):
    for c in cmds:
        resp = send_at(c, timeout=timeout).decode('utf-8','ignore').split('\r\n')
        print("resp:", resp)


def power_cycle(pin_number=MODEM_PWR):

    pwr_pin = Pin(MODEM_PWR, Pin.OUT)

    rc = send_at("AT+CPOWD=1")
    print("+CPOWD:", rc)

    pwr_pin.on()
    time.sleep(2)
    pwr_pin.off()
    time.sleep(2)

    rc = send_at("AT")
    print("AT:", rc)




# send_at('at+csq')  > 10

cmds = [
    "AT",             
    "AT+CFUN=1",
    'AT+SAPBR=3,1,"CONTYPE","GPRS"',
    # AT+SAPBR=3,1,"APN","your_apn",
    "AT+SAPBR=1,1",     # gprs session
    "AT+SAPBR=2,1"      # get status
]

http = [
    "at+httpinit",
    'at+HTTPPARA?',
    'AT+HTTPPARA="USERDATA","Accept: application/json"',
    'at+httppara="URL","http://rs.angara.net/meteo/_in"',
    'AT+HTTPPARA="USERDATA","Authorization: Basic dXNlcjpwYXNz\r\n"',
    'at+httpaction=0',
    'at+httpread',
    'at+httpterm'
]

clo = [
    'at+AT+SAPBR=0,1'
]

# send_cmds(http, timeout=2000)
