import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = '6618709244:AAGw5yx1rpj3BEEfFpqTawBpe8OvA-xe-TQ'
URL = "https://auto.ria.com/search/?indexName=auto,order_auto,newauto_search&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=-1&dealer.id=135&page=1&size=100"
previous_cars = []

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_current_cars():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    total_cars_element = soup.find('span', class_='staticResultsCount')
    
    if total_cars_element:
        return int(total_cars_element.text.strip())
    return 0

def compare_car_lists(prev, current):
    new_cars = [car for car in current if car not in prev]
    removed_cars = [car for car in prev if car not in current]
    return new_cars, removed_cars

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    check_btn = InlineKeyboardButton("Проверить автомобили", callback_data="check_cars")
    keyboard.add(check_btn)
    await message.answer("Привет! Я бот для отслеживания изменений в ассортименте вашего автосалона на auto.ria.ua.", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "check_cars")
async def check_changes(callback_query: types.CallbackQuery):
    global previous_cars
    current_cars = get_current_cars()
    new_cars, removed_cars = compare_car_lists(previous_cars, current_cars)
    
    if new_cars:
        for car in new_cars:
            await bot.send_message(callback_query.from_user.id, f"Новый автомобиль: {car}", parse_mode=ParseMode.HTML)
    if removed_cars:
        for car in removed_cars:
            await bot.send_message(callback_query.from_user.id, f"Автомобиль был удален: {car}", parse_mode=ParseMode.HTML)
    
    await bot.send_message(callback_query.from_user.id, f"Текущее количество опубликованных автомобилей: {len(current_cars)}")
    previous_cars = current_cars

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
