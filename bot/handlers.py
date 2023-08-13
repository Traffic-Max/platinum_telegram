# bot/handlers.py:
from aiogram import Dispatcher, types
from bot.utils import check_publications
from config.settings import bot, dp



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
    # ваш код
    pass
