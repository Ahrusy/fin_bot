# handlers.py
import random
import requests
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import main_keyboard
from states import FinancesForm
from database import get_user, register_user, save_finances

# Старт
async def send_start(message: Message):
    await message.answer(
        "Привет! Я ваш личный финансовый помощник. Выберите одну из опций:",
        reply_markup=main_keyboard
    )

# Регистрация
async def registration(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    user = get_user(telegram_id)

    if user:
        await message.answer("Вы уже зарегистрированы!")
    else:
        register_user(telegram_id, name)
        await message.answer("Вы успешно зарегистрированы!")

# Курсы валют
async def exchange_rates(message: Message):
    url = "https://v6.exchangerate-api.com/v6/09edf8b2bb246e1f801cbfba/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Не удалось получить курс валют.")
            return

        usd_to_rub = data["conversion_rates"]["RUB"]
        eur_to_usd = data["conversion_rates"]["EUR"]
        eur_to_rub = eur_to_usd * usd_to_rub

        await message.answer(
            f"1 USD = {usd_to_rub:.2f} RUB\n1 EUR = {eur_to_rub:.2f} RUB"
        )
    except:
        await message.answer("Произошла ошибка при получении курса.")

# Советы по экономии
async def send_tips(message: Message):
    tips = [
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам."
    ]
    await message.answer(random.choice(tips))

# Личные финансы — FSM
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.answer("Введите первую категорию расходов:")

async def process_category1(message: Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.answer("Введите расходы по категории 1:")

async def process_expenses1(message: Message, state: FSMContext):
    await state.update_data(expenses1=float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.answer("Введите вторую категорию расходов:")

async def process_category2(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.answer("Введите расходы по категории 2:")

async def process_expenses2(message: Message, state: FSMContext):
    await state.update_data(expenses2=float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.answer("Введите третью категорию расходов:")

async def process_category3(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.answer("Введите расходы по категории 3:")

async def process_expenses3(message: Message, state: FSMContext):
    data = await state.update_data(expenses3=float(message.text))
    user_data = await state.get_data()
    telegram_id = message.from_user.id

    save_finances(telegram_id, user_data)
    await state.clear()
    await message.answer("Категории и расходы сохранены!")
