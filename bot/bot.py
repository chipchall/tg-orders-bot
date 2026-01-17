import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHANNEL_ID = int(os.getenv("ADMIN_CHANNEL_ID"))  # обязательно int для канала

bot = telebot.TeleBot(BOT_TOKEN)

user_files = {}  # тут храним файлы для каждого пользователя

def main_menu(user_id):
    markup = InlineKeyboardMarkup()
    # Кнопка активна только если пользователь уже загрузил файлы
    if user_id in user_files and user_files[user_id]:
        markup.add(InlineKeyboardButton("Оформить заказ", callback_data="send_order"))
    else:
        markup.add(InlineKeyboardButton("Оформить заказ (нужно загрузить файлы)", callback_data="disabled"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    welcome_text = """
Здравствуйте.
Я занимаюсь выполнением чертежей и 3D-моделированием для учебных и коммерческих задач.

Через этого бота вы можете оформить заявку:
— с описанием задачи  
— с исходными файлами  
— без лишней переписки  

После оценки я напишу вам лично с ценой и сроками.
"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(user_id))

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    if user_id not in user_files:
        user_files[user_id] = []
    user_files[user_id].append((message.document.file_name, downloaded_file))

    bot.send_message(message.chat.id, "Файл получен. Кнопка оформления заказа теперь активна.", reply_markup=main_menu(user_id))

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    if call.data == "send_order":
        if user_id not in user_files or not user_files[user_id]:
            bot.answer_callback_query(call.id, "Сначала загрузите хотя бы один файл!")
            return
        for fname, fbytes in user_files[user_id]:
            bot.send_document(ADMIN_CHANNEL_ID, fbytes, caption=f"Файл от {call.from_user.username} / {user_id}: {fname}")
        bot.answer_callback_query(call.id, "Заявка отправлена!")
        user_files[user_id] = []
    elif call.data == "disabled":
        bot.answer_callback_query(call.id, "Сначала загрузите файлы!")

bot.infinity_polling()

