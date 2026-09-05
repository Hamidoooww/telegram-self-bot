import asyncio
import logging
from pyrogram import Client, idle
import config
from database.channel_db import restore_tasks_from_channel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def init_system():
    # اعتبارسنجی اولیه متغیرها
    if not config.API_ID or not config.API_HASH:
        logging.critical("API_ID or API_HASH is missing!")
        return
    if not config.SESSION_STRING:
        logging.critical("SESSION_STRING is empty! Authentication will fail.")
        return
    
    app = Client(
        "selfbot_session",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.SESSION_STRING,
        plugins=dict(root="plugins")
    )
    
    try:
        await app.start()
        logging.info("Client authenticated successfully.")
    except Exception as e:
        logging.critical(f"Failed to start client: {e}")
        return

    # (اختیاری) پیدا کردن کانال کانفیگ برای کش کردن
    if config.CONFIG_CHANNEL_ID != 0:
        logging.info("Searching for the config channel to populate peer cache...")
        try:
            async for dialog in app.get_dialogs():
                if dialog.chat.id == config.CONFIG_CHANNEL_ID:
                    logging.info("Config channel found and cached!")
                    break
        except Exception as e:
            logging.error(f"Error while fetching dialogs: {e}")
    else:
        logging.warning("CONFIG_CHANNEL_ID is not set. Task restoration will be skipped.")
    
    # بازیابی تسک‌ها (فقط در صورت وجود شناسه معتبر)
    if config.CONFIG_CHANNEL_ID != 0:
        logging.info("Restoring state from channel database...")
        await restore_tasks_from_channel(app, config.CONFIG_CHANNEL_ID)
    
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(init_system())