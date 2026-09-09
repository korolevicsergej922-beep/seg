import asyncio
import logging
import json
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

BOT_TOKEN = "8849749550:AAEKXnmAeKzPsFwyy93ItVFu7PmWE_7PA8g" # сюда токен бота вписываешь
ADMIN_IDS = [1560831396] #Сюда крч иды админов

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
logging.basicConfig(level=logging.INFO)

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": [], "total_users": 0, "registrations": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💛 Яндекс аккаунты", callback_data="yandex")],
    [InlineKeyboardButton(text="💜 WB аккаунты", callback_data="wb")],
    [InlineKeyboardButton(text="💳 Карты", callback_data="cards")],
    [InlineKeyboardButton(text="👤 Личный кабинет", callback_data="profile")],
    [InlineKeyboardButton(text="ℹ️ Канал с отзывами", url="https://t.me/scvirstio")]
])

back_btn = InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
buy_btn = InlineKeyboardButton(text="✅ Приобрести", callback_data="buy")

yandex_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Приобрести", callback_data="buy")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
])

wb_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Приобрести", callback_data="buy")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
])

cards_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💎 Хочу приобрести", callback_data="buy")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
])

payment_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💎 Crypto Bot", callback_data="pay_crypto")],
    [InlineKeyboardButton(text="🏦 Рубли (менеджер)", callback_data="pay_rubles")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
])

# Клавиатура для рублёвой оплаты
rubles_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✍️ Написать менеджеру", url="https://t.me/scvirsti")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
])

crypto_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✍️ Написать менеджеру", url="https://t.me/scvirsti")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
])

profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/scvirsti")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
])

ref_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
])

# ===== ОБРАБОТЧИКИ =====

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "нет"
    if user_id not in data["users"]:
        data["users"].append(user_id)
        data["total_users"] += 1
        data["registrations"].append({
            "id": user_id,
            "username": username,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_data(data)
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "╔ Мы продаем сплит аккаунты на Яндекс маркете и Wildberries.\n"
        "╚ Загляните в наш канал, чтобы посмотреть отзывы 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Перейти в канал", url="https://t.me/scvirstio")]
        ])
    )
    await message.answer(
        "Выберите нужный раздел 👇",
        reply_markup=main_kb
    )

@dp.callback_query(F.data == "back_to_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите нужный раздел 👇",
        reply_markup=main_kb
    )
    await callback.answer()

@dp.callback_query(F.data == "yandex")
async def yandex_menu(callback: CallbackQuery):
    text = (
        "💛 Яндекс маркет\n\n"
        "🔸 30к сплит - 2000\n"
        "🔸 50к сплит - 3000\n\n"
        "За более большими суммами обговаривать с менеджером."
    )
    await callback.message.edit_text(text, reply_markup=yandex_kb)
    await callback.answer()

@dp.callback_query(F.data == "wb")
async def wb_menu(callback: CallbackQuery):
    text = (
        "💜 Wildberries\n\n"
        "🔹 50к сплит - 3000\n"
        "🔹 75к сплит - 4500\n"
        "🔹 100к сплит - 6000\n"
        "🔹 150к сплит - 8500\n\n"
        "За более большими суммами обговаривать с менеджером."
    )
    await callback.message.edit_text(text, reply_markup=wb_kb)
    await callback.answer()

@dp.callback_query(F.data == "cards")
async def cards_menu(callback: CallbackQuery):
    text = (
        "💳 Карты\n\n"
        "💍 Ю мани - 1500 💍\n\n"
        "Нужен другой банк? Обратитесь за помощью к менеджеру."
    )
    await callback.message.edit_text(text, reply_markup=cards_kb)
    await callback.answer()

@dp.callback_query(F.data == "buy")
async def buy_payment(callback: CallbackQuery):
    await callback.message.edit_text(
        "💳 Выберите способ оплаты\n\n"
        "┌ 💎 Crypto — оплата через Crypto Bot\n"
        "└ 🏦 Рубли — оплата через менеджера",
        reply_markup=payment_kb
    )
    await callback.answer()

@dp.callback_query(F.data == "pay_crypto")
async def pay_crypto(callback: CallbackQuery):
    await callback.message.edit_text(
        "💎 Оплата криптовалютой\n\n"
        "┌ Для оплаты свяжитесь\n"
        "└ с нашим менеджером 👇",
        reply_markup=crypto_kb
    )
    await callback.answer()

@dp.callback_query(F.data == "pay_rubles")
async def pay_rubles(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏦 Оплата рублями\n\n"
        "┌ Для оплаты рублями свяжитесь\n"
        "└ с нашим менеджером 👇",
        reply_markup=rubles_kb
    )
    await callback.answer()

@dp.callback_query(F.data == "profile")
async def profile_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or "нет"
    reg_date = "неизвестно"
    for reg in data["registrations"]:
        if reg["id"] == user_id:
            reg_date = reg["date"]
            break
    invited = 0  
    text = (
        f"👤 Личный кабинет\n\n"
        f"🆔 ID: {user_id}\n"
        f"👤 Username: @{username}\n"
        f"📅 Дата регистрации: {reg_date}\n"
        f"👥 Всего приглашено: {invited} чел."
    )
    await callback.message.edit_text(text, reply_markup=profile_kb)
    await callback.answer()

@dp.callback_query(F.data == "ref")
async def ref_system(callback: CallbackQuery):
    user_id = callback.from_user.id
    ref_link = f"https://t.me/юз?start=ref_{user_id}"
    await callback.message.edit_text(
        f"👥 Реферальная система\n\n"
        f"Ваша реферальная ссылка:\n{ref_link}\n\n"
        f"Приглашайте друзей и получайте бонусы!",
        reply_markup=ref_kb
    )
    await callback.answer()

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()

@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔️ Доступ запрещён.")
        return
    stats = (
        f"📊 Статистика бота\n\n"
        f"👥 Всего пользователей: {data['total_users']}\n"
        f"📅 Зарегистрировано сегодня:\n"
        f"🆔 Ваш ID: {message.from_user.id}"
    )
    admin_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить сообщение всем", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="📊 Обновить статистику", callback_data="admin_stats")]
    ])
    await message.answer(stats, reply_markup=admin_kb)

@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔️ Нет прав", show_alert=True)
        return
    stats = f"👥 Всего пользователей: {data['total_users']}"
    await callback.message.edit_text(stats, reply_markup=None)
    await callback.answer()

@dp.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔️ Нет прав", show_alert=True)
        return
    await callback.message.edit_text("✍️ Введите текст для рассылки (всем пользователям):")
    await state.set_state(AdminStates.waiting_for_broadcast)
    await callback.answer()

@dp.message(AdminStates.waiting_for_broadcast)
async def send_broadcast(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔️ Нет прав")
        return
    text = message.text
    success = 0
    for uid in data["users"]:
        try:
            await bot.send_message(uid, text)
            success += 1
        except:
            pass
    await message.answer(f"✅ Рассылка завершена. Отправлено {success} пользователям.")
    await state.clear()

async def main():
    print("Бот Frogmen запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
