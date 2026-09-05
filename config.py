import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")   # مطابق با secrets
CONFIG_CHANNEL_ID = int(os.environ.get("CONFIG_CHANNEL_ID", 0))