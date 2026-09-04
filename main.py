import asyncio

# ساخت Event Loop به صورت دستی برای جلوگیری از خطای پایتون ۳.۱۴
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import logging
from pyrogram import Client, idle
import config
from database.channel_db import restore_tasks_from_channel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def init_system():
    app = Client(
        "selfbot_session",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.SESSION_STRING,
        plugins=dict(root="plugins")
    )
    
    await app.start()
    logging.info("Client authenticated successfully.")
    
    # --- بخش جدید: پیدا کردن کانال و ثبت در حافظه (رفع خطای KeyError) ---
    logging.info("Searching for the config channel to populate peer cache...")
    channel_found = False
    async for dialog in app.get_dialogs():
        if dialog.chat.id == config.CONFIG_CHANNEL_ID:
            channel_found = True
            logging.info("Config channel found and cached!")
            break
            
    if not channel_found:
        logging.warning("Config channel not found in your recent dialogs! Make sure the ID is correct.")
    # ------------------------------------------------------------------
    
    logging.info("Restoring state from channel database...")
    await restore_tasks_from_channel(app, config.CONFIG_CHANNEL_ID)
    
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(init_system())