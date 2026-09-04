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
            
            # بررسی اینکه خروجی حتماً یک دیکشنری باشد تا از خطای AttributeError جلوگیری شود
            if isinstance(data, dict):
                if data.get("action") == "SEND_PERIODIC":
                    task_hash = data.get("task_hash")
                    
                    # در صورتی که دیتای پیام ناقص باشد، از آن عبور کن
                    if not task_hash or "chat_id" not in data or "interval" not in data:
                        continue

                    task_obj = asyncio.create_task(
                        periodic_sender(app, data["chat_id"], data.get("text", ""), data["interval"], task_hash)
                    )
                    store.add_task(task_hash, task_obj, message.id)
                    count += 1
        except json.JSONDecodeError:
            continue
            
    logging.info(f"Successfully restored {count} active tasks from database.")