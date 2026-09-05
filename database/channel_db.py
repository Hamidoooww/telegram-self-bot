import json
import asyncio
import logging
from pyrogram import Client
from pyrogram.errors import ChannelInvalid, ChatIdInvalid
from core.memory import store
from core.worker import periodic_sender

async def restore_tasks_from_channel(app: Client, channel_id: int):
    """پیمایش کانال، استخراج JSON و راه‌اندازی مجدد تسک‌ها"""
    count = 0
    try:
        async for message in app.get_chat_history(channel_id):
            if not message.text:
                continue
            try:
                data = json.loads(message.text)
                if isinstance(data, dict) and data.get("action") == "SEND_PERIODIC":
                    task_hash = data.get("task_hash")
                    if not task_hash or "chat_id" not in data or "interval" not in data:
                        continue
                    task_obj = asyncio.create_task(
                        periodic_sender(app, data["chat_id"], data.get("text", ""), data["interval"], task_hash)
                    )
                    store.add_task(task_hash, task_obj, message.id)
                    count += 1
            except json.JSONDecodeError:
                continue
    except (ChannelInvalid, ChatIdInvalid) as e:
        logging.error(f"Cannot access config channel (ID: {channel_id}): {e}")
    except Exception as e:
        logging.error(f"Unexpected error while restoring tasks: {e}")
    else:
        logging.info(f"Successfully restored {count} active tasks from database.")