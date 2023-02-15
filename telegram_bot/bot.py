import logging
import os
from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()
bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)



if __name__ == '__main__':
    from handlers.handlers import dp

    executor.start_polling(dp)