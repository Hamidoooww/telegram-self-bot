import asyncio
import logging
from pyrogram import Client, idle
import config
from database.channel_db import restore_tasks_from_channel

# پیکربندی لاگ‌گیری برای دیباگ بهتر روی هاست ابری
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def init_system():
    # راه‌اندازی کلاینت و مسیردهی پوشه پلاگین‌ها
    app = Client(
        "selfbot_session",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.SESSION_STRING,
        plugins=dict(root="plugins")
    )
    
    await app.start()
    logging.info("Client authenticated successfully.")
    
    # فراخوانی لودر دیتابیس
    logging.info("Restoring state from channel database...")
    await restore_tasks_from_channel(app, config.CONFIG_CHANNEL_ID)
    
    # باز نگه داشتن حلقه رویداد
    await idle()
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.run(init_system())
