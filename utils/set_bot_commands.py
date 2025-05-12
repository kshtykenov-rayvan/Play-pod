from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.enums import BotCommandScopeType
import logging
from data.config import ADMINS
from dotenv import load_dotenv

load_dotenv()

async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Помощь"),
    ]

    admin_commands = [
        BotCommand(command="/admin", description="[ADMIN]Панель администратора"),
    ]

    try:
        await bot.set_my_commands(
            commands=commands,
            scope={"type": BotCommandScopeType.DEFAULT}
        )

        for admin in ADMINS:
            try:
                await bot.set_my_commands(
                    commands=commands + admin_commands,
                    scope={"type": BotCommandScopeType.CHAT, "chat_id": admin}
                )
            except Exception as err:
                logging.error(f"💢 Error setting commands for admin {admin}: {err}")

    except Exception as e:
        logging.error(f"💢 Error setting commands: {e}")