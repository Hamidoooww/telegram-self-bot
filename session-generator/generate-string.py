import asyncio
import sys

# ایجاد Event Loop به صورت دستی برای جلوگیری از خطای پایتون‌های جدید
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client

async def main():
    print("--- String Session Generator ---")
    api_id = input("Enter API ID: ")
    api_hash = input("Enter API HASH: ")

    app = Client(":memory:", api_id=int(api_id), api_hash=api_hash)
    
    await app.start()
    session_string = await app.export_session_string()
    
    print("\n✅ Authentication Successful!")
    print("👇 Your String Session (Copy this): 👇\n")
    print(session_string)
    
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())