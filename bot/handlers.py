# bot/handlers.py:
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils import check_publications
from config.settings import bot, dp
from database.db_session import SessionLocal
from database.models import Car


@dp.callback_query_handler(lambda c: c.data == 'publications')
async def process_callback_publications(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    new_links, removed_links = check_publications()
    
    session = SessionLocal()
    total_cars = session.query(Car).count()
    session.close()
    
    new_cars = len(new_links)
    removed_cars = len(removed_links)
    
    await bot.send_message(callback_query.from_user.id, f"Всего машин: {total_cars}\nНовые: {new_cars}\nУдаленные: {removed_cars}")
    
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton("Новые", callback_data='new_cars') # type: ignore
    item2 = InlineKeyboardButton("Удаленные", callback_data='removed_cars') # type: ignore
    markup.add(item1, item2)
    await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'new_cars')
async def show_new_cars(callback_query: types.CallbackQuery):
    new_links, _ = check_publications()
    for link in new_links:
        await bot.send_message(callback_query.from_user.id, f"Новое авто: {link}")


@dp.callback_query_handler(lambda c: c.data == 'removed_cars')
async def show_removed_cars(callback_query: types.CallbackQuery):
    _, removed_links = check_publications()
    for link in removed_links:
        await bot.send_message(callback_query.from_user.id, f"Удаленное авто: {link}")


@dp.callback_query_handler(lambda c: c.data == 'monitoring')
async def process_callback_monitoring(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Функция в разработке")
