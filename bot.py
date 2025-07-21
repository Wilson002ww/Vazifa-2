import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

API_TOKEN = '8019687026:AAGMunFRDF8_7Adgku46o4coUKUqw_ABLvk'
bot = telebot.TeleBot(API_TOKEN)

def get_categories():
    conn = sqlite3.connect("films.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    data = cursor.fetchall()
    conn.close()
    return data

def get_films_by_category(category_id):
    conn = sqlite3.connect("films.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, description FROM films WHERE category_id = ?", (category_id,))
    data = cursor.fetchall()
    conn.close()
    return data

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    for cat_id, name in get_categories():
        markup.add(InlineKeyboardButton(text=name, callback_data=f"cat_{cat_id}"))
    bot.send_message(message.chat.id, "Kategoriya tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def callback_query(call):
    cat_id = int(call.data.split("_")[1])
    films = get_films_by_category(cat_id)
    if films:
        text = "\n\n".join([f"🎬 {title}\n📄 {desc}" for title, desc in films])
    else:
        text = "Bu kategoriyada filmlar mavjud emas."
    bot.send_message(call.message.chat.id, text)

bot.polling()
