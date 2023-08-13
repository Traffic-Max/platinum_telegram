from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from bot.utils import check_publications
from database.db_session import init_db


TOKEN = '6618709244:AAGw5yx1rpj3BEEfFpqTawBpe8OvA-xe-TQ'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

init_db()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton("Публикации", callback_data='publications') # type: ignore
    item2 = InlineKeyboardButton("Мониторинг", callback_data='monitoring') # type: ignore
    markup.add(item1, item2)
    await message.answer("Добро пожаловать!", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'publications')
async def process_callback_publications(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    new_links, removed_links = check_publications()
    if new_links or removed_links:
        await bot.send_message(callback_query.from_user.id, "Есть изменения!")
        # Здесь можно добавить кнопки для показа новых и удаленных ссылок
    else:
        await bot.send_message(callback_query.from_user.id, "Нет изменений.")

@dp.callback_query_handler(lambda c: c.data == 'monitoring')
async def process_callback_monitoring(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Функция в разработке")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
