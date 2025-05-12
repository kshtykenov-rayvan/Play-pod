import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS = [int(admin_id) for admin_id in os.getenv("ADMIN_ID", "").split(",") if admin_id]

OPEN_AI_API = os.getenv("OPEN_AI_API")

DATABASE_URL = "sqlite+aiosqlite:///playpad.db"

if __name__ == "__main__":
    print(BOT_TOKEN)
    print(ADMINS)
    print(OPEN_AI_API)