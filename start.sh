#!/bin/bash
export BOT_TOKEN="8217026061:AAFMftJcVJcMq7tx5bWuWzaTRGtRl2UiO80"
export ADMIN_CHANNEL_ID="-1001234567890"

# Активируем виртуальное окружение
source .venv/bin/activate

# Запускаем бота
python3 bot/bot.py

