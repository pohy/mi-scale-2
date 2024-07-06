from os import path, makedirs
from dotenv import dotenv_values

config_path = path.join(path.dirname(__file__), '..', '.env')
config = dotenv_values(config_path)

DATA_DIR = config.get('DATA_DIR', path.join(path.dirname(__file__), '..', 'data'))
# Ensure that data dir exists
if not path.exists(DATA_DIR):
    makedirs(DATA_DIR)


ENV = config.get('ENV', 'development')
IS_PRODUCTION = ENV == 'production'
PORT = config.get('PORT', 80 if IS_PRODUCTION else 1337)
PORT = int(PORT)
LOG_LEVEL = config.get('LOG_LEVEL', 'INFO')

MAC_ADDRESS = config.get('MAC_ADDRESS', None)
TIMEOUT = float(config.get('TIMEOUT', 0.2))
SCAN_FREQUENCY_HZ = int(config.get('SCAN_FREQUENCY_HZ', 10))
MIN_WEIGHT = float(config.get('MIN_WEIGHT', 0.0))
MAX_WEIGHT = float(config.get('MAX_WEIGHT', 1000.0))

TELEGRAM_BOT_TOKEN = config.get('TELEGRAM_BOT_TOKEN', None)
TELEGRAM_CHAT_ID = config.get('TELEGRAM_CHAT_ID', None)

CHANGE_TRENDS_DAYS = [7, 14, 30, 90]

SPREADSHEET_URL = config.get('SPREADSHEET_URL', '')
