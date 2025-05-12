import os
import subprocess
import uuid

def download_audio_from_youtube(url: str) -> str:
    unique_id = str(uuid.uuid4())[:8]
    output_template = f"downloads/{unique_id}.%(ext)s"
    final_path = f"downloads/{unique_id}.mp3"

    try:
        os.makedirs("downloads", exist_ok=True)

        result = subprocess.run(
            [
                "yt-dlp",
                "--cookies", "cookies.txt",        # ← авторизация
                "-x", "--audio-format", "mp3",
                "-o", output_template,
                url
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("[yt-dlp stderr]:", result.stderr)
            print("[yt-dlp stdout]:", result.stdout)
            print("[Ошибка] yt-dlp завершился с кодом:", result.returncode)
            return None

        if os.path.exists(final_path):
            print(f"[Успешно] mp3 сохранён: {final_path}")
            return final_path
        else:
            print("[Ошибка] mp3-файл не найден.")
            return None

    except Exception as e:
        print(f"[Исключение] yt-dlp сломался: {e}")
        return None