import json
import asyncio
import logging
from pyrogram import Client
from core.memory import store
from core.worker import periodic_sender

async def restore_tasks_from_channel(app: Client, channel_id: int):
    """پیمایش کانال، استخراج JSON و راه‌اندازی مجدد تسک‌ها"""
    count = 0
    async for message in app.get_chat_history(channel_id):
        if not message.text:
            continue
        try:
            data = json.loads(message.text)
            if data.get("action") == "SEND_PERIODIC":
                task_hash = data["task_hash"]
                task_obj = asyncio.create_task(
                    periodic_sender(app, data["chat_id"], data["text"], data["interval"], task_hash)
                )
                store.add_task(task_hash, task_obj, message.id)
                count += 1
        except json.JSONDecodeError:
            continue
    logging.info(f"Successfully restored {count} active tasks from database.")
