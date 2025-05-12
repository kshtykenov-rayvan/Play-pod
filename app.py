from aiogram import Dispatcher
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from data.config import BOT_TOKEN
import handlers
import asyncio
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import logging


dp = Dispatcher()

async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
        timeout=30.0
    )

    handlers.setup(dp)

    await on_startup_notify(bot)

    await set_default_commands(bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())