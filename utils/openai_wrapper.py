import openai
from data.config import OPEN_AI_API

def call_openai_chat(
    api_key: str, # Ключ OpenAI.
    messages: list, # Список сообщений в формате [{'role': 'user', 'content': 'Привет!'}, ...]
    model: str = "gpt-4", # Модель OpenAI (gpt-4, gpt-3.5-turbo и т.д.)
    temperature: float = 0.7, # Креативность (0.0 – точно, 1.0 – свободно)
    max_tokens: int = 1024, # Максимум токенов в ответе
    top_p: float = 1.0, # Альтернатива temperature, верояggfghтностный срез
    frequency_penalty: float = 0.0, # Штраф за повтор d
    presence_penalty: float = 0.0, # Начальная инструкция (например, стиль, роль)
    system_prompt: str = "You are a helpful assistant.", # Имя пользователя (для логики)
    user_name: str = "user", # Список стоп-токенов для остановки генерации
    stop: list = None # Ответ модели (str)
):
    
    openai.api_key = api_key

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    response = openai.ChatCompletion.create(
        model=model,
        messages=full_messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
        user=user_name
    )

    return response['choices'][0]['message']['content']


if __name__ == "__main__":
    response = call_openai_chat(
        api_key=f"{OPEN_AI_API}",
        messages=[{"role": "user", "content": "Объясни квантовую запутанность"}],
        system_prompt="Ты — язвительный, но гениальный научный ассистент.",
        temperature=0.9,
        model="gpt-4",
        max_tokens=512
    )

    print(response)