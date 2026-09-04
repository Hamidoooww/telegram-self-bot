import os
from dotenv import load_dotenv

# این خط الزامی است؛ بدون آن فایل .env نادیده گرفته می‌شود
load_dotenv()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")

# نام متغیر با فایل .env شما (STRING_SESSION) همگام‌سازی شد
SESSION_STRING = os.environ.get("STRING_SESSION", "")

CONFIG_CHANNEL_ID = int(os.environ.get("CONFIG_CHANNEL_ID", 0))