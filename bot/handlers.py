# bot/handlers.py:
from aiogram import Dispatcher, types
from bot.utils import check_publications
from config.settings import bot, dp

@dp.callback_query_handler(lambda c: c.data == 'publications')
async def process_callback_publications(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    new_links, removed_links = check_publications()
    if new_links:
        await bot.send_message(callback_query.from_user.id, "Новые публикации:")
        for link in new_links:
            await bot.send_message(callback_query.from_user.id, link)
    if removed_links:
        await bot.send_message(callback_query.from_user.id, "Удаленные публикации:")
        for link in removed_links:
            await bot.send_message(callback_query.from_user.id, link)
    if not new_links and not removed_links:
        await bot.send_message(callback_query.from_user.id, "Нет изменений.")


@dp.callback_query_handler(lambda c: c.data == 'monitoring')
async def process_callback_monitoring(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Функция в разработке")
