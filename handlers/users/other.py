from aiogram import Router
from aiogram.types import Message
from dotenv import load_dotenv
from data.config import OPEN_AI_API
from utils.openai_wrapper import call_openai_chat
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
import ast
import os

load_dotenv()
router = Router()

def extract_last_json_block(text):
    """
    Извлекает последний валидный словарь (JSON или Python dict) из текста
    """
    stack = []
    start = None
    for i, c in enumerate(text):
        if c == '{':
            if not stack:
                start = i
            stack.append(c)
        elif c == '}':
            stack.pop()
            if not stack and start is not None:
                candidate = text[start:i+1]
                try:
                    parsed = ast.literal_eval(candidate)
                    return text[:start].strip(), parsed
                except Exception:
                    continue
    raise ValueError("Не удалось извлечь валидный JSON или словарь.")

def split_message(input_text: str):
    """
    Делит сообщение на user_message и structured_data.
    Ищет последний словарь в тексте (многострочный, валидный).
    """
    user_message, structured_data = extract_last_json_block(input_text)

    if not isinstance(structured_data, dict) or "type" not in structured_data:
        raise ValueError("Блок найден, но не содержит ключ 'type'.")

    return {
        "user_message": user_message,
        "structured_data": structured_data
    }

def create_inline_keyboard_from_list(titles: list[str], buttons_per_row: int = 2):
    """
    Создаёт InlineKeyboardMarkup, где каждая кнопка — это элемент списка.
    buttons_per_row — сколько кнопок в одном ряду
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    row = []
    for idx, title in enumerate(titles):
        button = InlineKeyboardButton(text=title, callback_data=f"track_{idx}")
        row.append(button)
        if len(row) == buttons_per_row:
            keyboard.inline_keyboard.append(row)
            row = []
    
    # добавляем остатки
    if row:
        keyboard.inline_keyboard.append(row)
    
    return keyboard

@router.message()
async def other(message: Message):
    user_id = message.from_user.id
    user_input = message.text

    response = call_openai_chat(
        api_key=OPEN_AI_API,
        messages=[{"role": "user", "content": user_input}],
        system_prompt="""
Ты — Ники, музыкальный ассистент. Твоя задача — давать рекомендации пользователю и **отдельно** выводить JSON **только для машины**.

**Никогда не вставляй JSON внутрь сообщения.**
Сначала идёт обычный текст, затем — на новой строке — JSON.

Пример:
Конечно! Вот несколько треков:
1. Скриптонит — "Положение"
2. AIGEL — "Татарин"

{
  "type": "music_recommendation",
  "tracks": ["Скриптонит — Положение", "AIGEL — Татарин"]
}
""",
        temperature=0.9,
        model="gpt-4",
        max_tokens=512
    )

    try:
        result = split_message(response)
    except ValueError as e:
        await message.answer("Произошла ошибка при разборе ответа модели:\n" + str(e))
        return

    # JSON остаётся в логах или передаётся в БД
    # print(f"JSON STRUCTURED DATA (для БД):\n{result['structured_data']['tracks']}")
    titles = result['structured_data']['tracks']

    print()

    keyboard = create_inline_keyboard_from_list(titles)

    # Отправляем только текст
    await message.answer(f"{result["user_message"]}", reply_markup=keyboard)

from aiogram.types import CallbackQuery
from utils.tube_search import search_youtube
from utils.download_youtube import download_audio_from_youtube



@router.callback_query()
async def handle_track_selection(callback: CallbackQuery):
    await callback.answer("⏳ Обработка...")

    # Получаем индекс из callback_data
    data = callback.data
    if not data.startswith("track_"):
        await callback.message.answer("Некорректный формат callback.")
        return

    try:
        index = int(data.split("_")[1])
    except ValueError:
        await callback.message.answer("Не удалось определить выбранный трек.")
        return

    # Достаём из последнего сообщения названия треков
    # (мы предполагаем, что это всё ещё валидный контекст — упрощённо)
    keyboard_rows = callback.message.reply_markup.inline_keyboard
    flat_titles = [btn.text for row in keyboard_rows for btn in row]

    if index >= len(flat_titles):
        await callback.message.answer("Индекс трека выходит за пределы списка.")
        return

    track_name = flat_titles[index]
    await callback.message.answer(f"🔍 Ищу трек: *{track_name}*", parse_mode="Markdown")

    # Поиск по YouTube
    results = search_youtube(track_name)
    if not results:
        await callback.message.answer("Ничего не найдено.")
        return

    video_url = results[0]['link']
    await callback.message.answer(f"▶️ Нашёл: {video_url}")

    # Скачивание
    mp3_path = download_audio_from_youtube(video_url)
    if not mp3_path or not os.path.exists(mp3_path):
        await callback.message.answer("❌ Не удалось скачать трек.")
        return

    # Отправка файла
    await callback.message.answer_audio(audio=open(mp3_path, 'rb'), caption=track_name)

    # Очистка
    try:
        os.remove(mp3_path)
    except Exception as e:
        print(f"[warning] Не удалось удалить временный файл: {e}")