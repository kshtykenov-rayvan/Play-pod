import logging
from aiogram import Bot
from data.config import ADMINS
from dotenv import load_dotenv  # Add this import

load_dotenv()

async def on_startup_notify(bot: Bot):
    message = "🔥 Бот запущен и готов к работе! "
    try:
        for admin in ADMINS:
            try:
                await bot.send_message(admin, message)
            except Exception as err:
                logging.error(f"💢 Failed to send message to admin {admin}. Error: {err}")
    except Exception as e:
        logging.error(f"💢 Error sending notifications to admins: {e}")