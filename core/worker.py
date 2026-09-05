import asyncio
import logging
from pyrogram import Client
from pyrogram.errors import FloodWait

async def periodic_sender(app: Client, chat_id: int, text: str, interval: int, task_hash: str):
    """حلقه ارسال پیام مستقل که در پس‌زمینه اجرا می‌شود"""
    try:
        while True:
            try:
                await app.send_message(chat_id=chat_id, text=text)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                logging.error(f"[{task_hash}] Worker Error: {e}")
            
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        logging.info(f"[{task_hash}] Task forcefully cancelled.")