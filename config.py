
VERSION = "ws_espy v2025.10.12"

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


env = load_dotenv() or {}

SUBMIT_URL  = env.get("SUBMIT_URL", "http://rs.angara.net/meteo/_in")
SUBMIT_USER = env.get("SUBMIT_USER", "")
SUBMIT_PASS = env.get("SUBMIT_PASS", "")

WIFI_SSID = env.get("WIFI_SSID")
WIFI_PASS = env.get("WIFI_PASS")

GPRS_APN  = env.get("GPRS_APN", "internet.tele2.ru")

HWID = env.get("HWID")  # use machine.unique_id() instead

READ_TEMP = bool_val(env.get("READ_TEMP", "yes"))
READ_WIND = bool_val(env.get("READ_WIND", "yes"))

BOARD = env.get("BOARD", "esp32")  # "esp32-c3"
