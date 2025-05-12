#!/bin/bash

# === НАСТРОЙКИ ===
ARCHIVE_NAME="project_backup_$(date +%Y-%m-%d_%H-%M-%S).zip"

echo "===[ АРХИВАЦИЯ ПРОЕКТА В ZIP ]==="
echo "[1/2] Удаляю .git (если есть)..."
rm -rf .git

echo "[2/2] Упаковываю проект в $ARCHIVE_NAME ..."
zip -r "$ARCHIVE_NAME" . -x "*.DS_Store" -x "$ARCHIVE_NAME" -x "*.zip" -x "__pycache__/*"

echo "===[ ГОТОВО: АРХИВ СОЗДАН → $ARCHIVE_NAME ]==="