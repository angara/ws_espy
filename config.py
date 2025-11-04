
VERSION = "ws_espy/2025.11.04"

def split_pair(s):
    s = s.strip()
    if s and s[0] != "#":
        pair = s.split('=')
        return (pair[0].strip(), pair[1].strip()) if pair else None

def load_dotenv(dotenv_path=".env") -> dict[str, str] | None:
    try:
        with open(dotenv_path, 'r') as file:
            pairs = (split_pair(s) for s in file.readlines())
            return dict(p for p in pairs if p)
    except OSError:
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

WIFI      = env.get("WIFI")
WIFI_SSID = env.get("WIFI_SSID")
WIFI_PASS = env.get("WIFI_PASS")

GPRS     = env.get("GPRS")
GPRS_APN = env.get("GPRS_APN")

HWID = env.get("HWID")  # use machine.unique_id() instead

READ_TEMP = bool_val(env.get("READ_TEMP", "yes"))
READ_WIND = bool_val(env.get("READ_WIND", "yes"))

BOARD = env.get("BOARD", "esp32")
