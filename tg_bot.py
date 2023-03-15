from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import os
from database import DataBasePostgres as bd


load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot)

