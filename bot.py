# bot.py
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, Command
from aiogram import F

from config import TOKEN
from database import init_db
from states import FinancesForm
import handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

def register_handlers():
    dp.message.register(handlers.send_start, CommandStart())
    dp.message.register(handlers.registration, F.text == "Регистрация в телеграм боте")
    dp.message.register(handlers.exchange_rates, F.text == "Курс валют")
    dp.message.register(handlers.send_tips, F.text == "Советы по экономии")
    dp.message.register(handlers.finances, F.text == "Личные финансы")

    dp.message.register(handlers.process_category1, FinancesForm.category1)
    dp.message.register(handlers.process_expenses1, FinancesForm.expenses1)
    dp.message.register(handlers.process_category2, FinancesForm.category2)
    dp.message.register(handlers.process_expenses2, FinancesForm.expenses2)
    dp.message.register(handlers.process_category3, FinancesForm.category3)
    dp.message.register(handlers.process_expenses3, FinancesForm.expenses3)

async def main():
    init_db()
    register_handlers()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
