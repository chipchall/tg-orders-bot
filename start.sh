#!/bin/bash
# Устанавливаем зависимости (Render обычно сам делает, но пусть будет)
pip install -r requirements.txt

# Запускаем сервер
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
