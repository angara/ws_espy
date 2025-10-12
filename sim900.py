
from machine import UART, Pin
import time
from ubinascii import b2a_base64

from conn import split_url
import config

MODEM_TX  = 12  # D2
MODEM_RX  = 14  # D3
MODEM_PWR = 13  # D8

# uart = UART(1, tx=Pin(22), rx=Pin(23))
uart = UART(1, 9600, tx=MODEM_TX, rx=MODEM_RX)


def power_cycle(pin_number=MODEM_PWR):

    pwr_pin = Pin(MODEM_PWR, Pin.OUT)

    while uart.any():
        uart.read()

    uart.write("AT+CPOWD=1\r\n")
    time.sleep(1)
    rc = uart.read()
    print("+CPOWD:", rc)

    pwr_pin.on()
    time.sleep(2)
    pwr_pin.off()
    time.sleep(2)

    uart.write("AT\r\n")
    time.sleep(1)
    rc = uart.read()
    print("AT:", rc)


def tcp_send(uart:UART, apn:str, host:str, port:int, data_to_send) -> str:
    """
    Returns:
        Response string from remote server or error message.
    """

    def send_cmd(cmd, delay=1, expected="OK"):
        uart.write(cmd + "\r\n")
        time.sleep(delay)
        resp = uart.read()
        if resp:
            resp_str = resp.decode()
            print(">>", resp_str.strip())
            if expected in resp_str:
                return resp_str
        return None

    # 1. Basic init
    send_cmd("AT")
    send_cmd("ATE0")  # Echo off

    # 2. Attach to GPRS
    send_cmd('AT+CGATT=1', 2)

    # 3. Set up PDP context (GPRS connection)
    send_cmd(f'AT+CSTT="{apn}"', 2)
    send_cmd("AT+CIICR", 5)  # Bring up wireless connection
    send_cmd("AT+CIFSR", 2)  # Get local IP address

    # 4. Start TCP connection
    if not send_cmd(f'AT+CIPSTART="TCP","{host}","{port}"', 6, "CONNECT OK"):
        return "TCP connection failed"

    # 5. Send data
    send_cmd("AT+CIPSEND", 2, ">")
    uart.write(data_to_send + "\x1A")  # Ctrl+Z to end sending
    time.sleep(4)
    resp = uart.read()
    if resp:
        print("Response after send:", resp.decode())

    # 6. Close connection
    send_cmd("AT+CIPCLOSE", 2)
    send_cmd("AT+CIPSHUT", 3)

    return "Done"


def send_http(url:str, auth:tuple[str,str], data:dict):

    parts = split_url(url)
    host, port, path = parts.get('host'), parts.get('port'), parts.get('path')

    qs = '&'.join([f'{k}={v}' for k,v in data.items() if v is not None])
    basic = 'Basic '+b2a_base64(f"{auth[0]}:{auth[1]}".encode()).decode().strip()
    req = f"GET /{path+'?'+qs} HTTP/1.0\r\nHost: {host}\r\nAuthorization: {basic}\r\n\r\n"

    rc = tcp_send(uart, config.GPRS_APN, host, port, req)
    if rc == "Done":
        return True
    else:
        power_cycle()
        time.sleep(5)
        rc = tcp_send(uart, config.GPRS_APN, host, port, req)
        return rc == "Done"
