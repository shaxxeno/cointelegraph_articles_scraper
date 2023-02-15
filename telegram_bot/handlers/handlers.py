from aiogram.types import Message
from dotenv import load_dotenv
from telegram_bot.bot import bot, dp
from classes.articles_data import Data
import os

load_dotenv()

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}!')

@dp.message_handler(commands=['get_articles'])
async def articles(message: Message):
    data = Data('../files/articles_urls.txt')
    data.save_urls()
    file = data.get_data()
    await bot.send_document(document=open(file, 'rb'), chat_id=message.chat.id)
    os.remove(file)
    os.remove(f'../files/articles_urls.txt')
