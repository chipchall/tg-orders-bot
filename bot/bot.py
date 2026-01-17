import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оформить заказ",
                    web_app=WebAppInfo(
                        url="https://ТУТ_БУДЕТ_ССЫЛКА"
                    )
                )
            ]
        ]
    )

    await message.answer(
        "Здравствуйте.\n"
        "Я занимаюсь выполнением чертежей и 3D-моделированием для учебных и коммерческих задач.\n\n"
        "Через этого бота вы можете оформить заявку:\n"
        "— с описанием задачи\n"
        "— с исходными файлами\n"
        "— без лишней переписки\n\n"
        "После оценки я напишу вам лично с ценой и сроками.",
        reply_markup=keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
