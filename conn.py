
import network
import time
from mrequests import request, Response


WIFI_RETRY_COUNT = 10
WIFI_RETRY_DELAY = 1
SUBMIT_TIMEOUT = 10


wifi = network.WLAN(network.STA_IF)

def mac2str(mac):
  return ''.join([f"{b:02x}" for b in mac])
#

def setup_wifi(ssid, password):
  if not ssid or ssid == "-":
    print("setup_wifi: wifi disabled")
    return "-"
  #
  if wifi.active() and wifi.isconnected():
    print("wifi connnected:", wifi.ipconfig('addr4'))
    return mac2str(wifi.config('mac'))
  else:
    wifi.active(False)
    wifi.active(True)
    wifi.connect(ssid, password)
    for _ in range(WIFI_RETRY_COUNT):
      if wifi.isconnected():
        return mac2str(wifi.config('mac'))
      print("wait for WiFi...")
      time.sleep(WIFI_RETRY_DELAY)
    return False
#

def query_string(data:dict) -> str:
    # NOTE: no escaping!
    return '&'.join([f'{k}={v}' for k,v in data.items() if v is not None])

def submit_data(url:str, auth:tuple, data:dict) -> Response:
  print(f"submit_data({url=})", data)
  qs = query_string(data)
  return request('GET', f'{url}?{qs}', auth=auth, timeout=SUBMIT_TIMEOUT)
#
