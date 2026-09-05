import asyncio
from pyrogram import Client

async def main():
    print("--- File Session Generator ---")
    api_id = input("Enter API ID: ")
    api_hash = input("Enter API HASH: ")
    session_name = input("Enter a name for this session (e.g., userbot_1): ")

    app = Client(session_name, api_id=int(api_id), api_hash=api_hash)
    await app.start()
    print(f"\n✅ Authentication Successful!")
    print(f"📁 Session file '{session_name}.session' generated in the current directory.")
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())