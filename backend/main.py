import os
import requests
from fastapi import FastAPI, UploadFile, Form
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("ADMIN_CHANNEL_ID")

app = FastAPI()

@app.post("/submit")
async def submit(
    user: str = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    files: list[UploadFile] = []
):
    text = (
        f"🆕 Новая заявка\n\n"
        f"👤 @{user}\n"
        f"📌 Тип: {type}\n\n"
        f"{description}"
    )

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHANNEL_ID, "text": text}
    )

    for file in files:
        content = await file.read()
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
            data={"chat_id": CHANNEL_ID},
            files={"document": (file.filename, content)}
        )

    return {"ok": True}
