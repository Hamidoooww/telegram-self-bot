import json
import uuid
import asyncio
from pyrogram import Client, filters
from config import CONFIG_CHANNEL_ID
from core.memory import store
from core.worker import periodic_sender

@Client.on_message(filters.me & filters.command("add", prefixes="."))
async def handle_add_task(client: Client, message):
    try:
        args = message.text.split(" ", 3)
        interval = int(args[1])
        target_chat_id = int(args[2])
        text_content = args[3]
        
        task_hash = str(uuid.uuid4())[:8]
        payload = {
            "task_hash": task_hash,
            "action": "SEND_PERIODIC",
            "chat_id": target_chat_id,
            "interval": interval,
            "text": text_content
        }
        
        # ثبت در دیتابیس کانال
        db_msg = await client.send_message(
            chat_id=CONFIG_CHANNEL_ID,
            text=json.dumps(payload, indent=2)
        )
        
        # ثبت در حافظه و اجرا
        task_obj = asyncio.create_task(
            periodic_sender(client, target_chat_id, text_content, interval, task_hash)
        )
        store.add_task(task_hash, task_obj, db_msg.id)
        
        await message.reply(f"✅ تسک ذخیره و اجرا شد. شناسه: `{task_hash}`")
    except Exception:
        await message.reply("فرمت اشتباه. الگو:\n`.add [interval] [chat_id] [text]`")

@Client.on_message(filters.me & filters.command("del", prefixes="."))
async def handle_delete_task(client: Client, message):
    try:
        task_hash = message.text.split(" ")[1]
        
        # حذف از حافظه و توقف پروسه
        msg_id = store.remove_task(task_hash)
        
        if msg_id:
            # حذف رکورد از دیتابیس کانال
            await client.delete_messages(CONFIG_CHANNEL_ID, msg_id)
            await message.reply(f"🗑 تسک `{task_hash}` متوقف و حذف شد.")
        else:
            await message.reply("شناسه نامعتبر است یا تسک فعال نیست.")
    except IndexError:
        await message.reply("فرمت اشتباه. الگو:\n`.del [hash]`")