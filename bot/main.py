# bot/main.py:
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from bot.utils import check_publications
from database.db_session import SessionLocal, init_db
from bot.handlers import *
from config.settings import bot, dp
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.models import Car

init_db()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton("Публикации", callback_data='publications') # type: ignore
    item2 = InlineKeyboardButton("Мониторинг", callback_data='monitoring') # type: ignore
    markup.add(item1, item2)
    await message.answer("Добро пожаловать!", reply_markup=markup)


async def check_links_periodically():
    new_links, removed_links = check_publications()
    chat_id = 389250313  # ваш chat_id
    
    if new_links:
        await bot.send_message(chat_id, "Новые публикации:")
        for link in new_links:
            await bot.send_message(chat_id, link)
    if removed_links:
        await bot.send_message(chat_id, "Удаленные публикации:")
        for link in removed_links:
            await bot.send_message(chat_id, link)
    if not new_links and not removed_links:
        await bot.send_message(chat_id, "Нет изменений.")


@dp.message_handler(commands=['update_db'])
async def update_database(message: types.Message):
    new_links, removed_links = check_publications()
    
    session = SessionLocal()
    
    # Удаляем все записи из базы данных
    session.query(Car).delete()
    
    # Добавляем все текущие ссылки в базу данных
    for link in new_links:
        new_car = Car(link=link)
        session.add(new_car)
    
    session.commit()
    session.close()
    
    await message.answer("База данных успешно обновлена!")

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_links_periodically, 'interval', hours=0.5)
    scheduler.start()

    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
