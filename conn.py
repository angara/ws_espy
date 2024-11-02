
import network
import time
import urequests


WIFI_RETRY_COUNT = 10
WIFI_RETRY_DELAY = 1

wifi = network.WLAN(network.STA_IF)


def mac2str(mac):
  return ''.join([f"{b:02x}" for b in mac])
#

def setup_wifi(ssid, password):
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

def submit_data(url, auth_basic, data):
  print(f"submit_data({url=})", data)
  # XXX: !!!
  return dict(err='err')
#
