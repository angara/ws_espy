
def load_dotenv(dotenv_path=".env") -> dict[str, str] | None:
    try:
        with open(dotenv_path, 'r') as file:
            return dict(line.rstrip().split('=')
                        for line in file if line.strip() and not line.startswith('#'))
    except FileNotFoundError:
        return None

TRUE_SET  = set(["true", "yes", "1"])
FALSE_SET = set(["false", "no", "0"])

def bool_val(s:str) -> bool | None:
    v = s.strip().lower()
    if v in TRUE_SET:
        return True
    if v in FALSE_SET:
        return False
    return None

ENV = load_dotenv() or {}

SUBMIT_URL  = ENV.get("SUBMIT_URL", "http://rs.angara.net/meteo/_in")
SUBMIT_USER = ENV.get("SUBMIT_USER", "")
SUBMIT_PASS = ENV.get("SUBMIT_PASS", "")

WIFI_SSID = ENV.get("WIFI_SSID", "-")
WIFI_PASS = ENV.get("WIFI_PASS", "")

HWID = ENV.get("HWID")  # use machine.unique_id() instead

READ_TEMP = bool_val(ENV.get("READ_TEMP", "yes"))
READ_WIND = bool_val(ENV.get("READ_WIND", "yes"))

BOARD = ENV.get("BOARD", "esp32")
# BOARD = "esp32-c3"
