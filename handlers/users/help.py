from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

router = Router()

@router.message(Command('help'))
async def help(message: Message):
    await message.answer('В этом проекте очень интуитивная управление в связи с тем что тут очень сильно внедрена системой AI.\n если у вас возникнут вопросы или же не такие осложнения или вы хотите поинтересоваться чем-то интересным связанное с моей работой и этим телеграмм потом а вы можете написать мне -> @alisher_kshtykenov')