from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer("""
Привет! Я — твой музыкальный проводник.
Просто расскажи, что тебе интересно — стиль, настроение, артист — и я подберу трек.
Сразу предупреждаю: из-за ограничений платформы, не все аудиофайлы я могу отправить напрямую.
Но ссылка на клип — всегда будет.
Никаких команд. Пиши, как человеку. Я отвечу как машина, которая понимает музыку.
""")