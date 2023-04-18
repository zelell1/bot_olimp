from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from Token import TOKEN
from aiogram.types.web_app_info import WebAppInfo
from init_db import User 
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])  # функция вызова сообщения с помощью
async def starting(message: types.Message):
    global user
    inf_user = message.from_user
    user = User(inf_user['id'], inf_user['first_name'], inf_user['last_name'], inf_user['username'])
    user.add_user()
    await message.answer(f"""<strong>Это персональный-бот помощник.</strong> 
Он будет помогать вам в отслеживании олимпиад.\t
С ним больше не беспокойтесь, что пропустите олимпиаду.""", parse_mode="HTML")
    

@dp.message_handler(commands=['add'])
async def olimpiads(message: types.Message):
    usern = user.usernam()
    url = 'http://127.0.0.1:8000/list_olimpix'
    response = requests.get(url=url).json()
    keyboard = types.InlineKeyboardMarkup()
    for elem in response:
        keyboard.add(types.InlineKeyboardButton(text=elem, callback_data=f"p:{elem}:{response.index(elem)}"))
    await message.answer(f"""Приветствую {usern}, теперь пожалуйста выберите профили предметов, в которые вас интересуют""", parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="p") 
async def find_in_prof(query: CallbackQuery):
    await query.answer()
    await query.message.delete()
    data = query.data.split(':')
    prof = data[-2]
    ind = int(data[-1])
    url = 'http://127.0.0.1:8000/olimpix'
    response = requests.get(url=url).json()
    await query.message.answer("""Когда будете выбирать олимпиады пожалуйста вводите через запятую уникальный номер олимпиад/олимпиады""", parse_mode="HTML")
    await query.message.answer("""Например 1,4,10,11 и т.д""", parse_mode="HTML")
    for i in response[ind][prof]:
        dataset = i["".join(list(i.keys()))]
        num = dataset[0]
        desc = dataset[1]
        level = dataset[2]
        uniq = dataset[-1].split('/')[-1]
        await query.message.answer(f"""<strong>Наименование олимпиады</strong>: {"".join(list(i.keys()))}  
<strong>№ в перечне</strong>:  {num}  
<strong>Предмет</strong>: {desc}  
<strong>Уровень</strong>: {level}
<strong>Уникальный номер</strong>: {uniq} """, parse_mode="HTML")



if __name__ == '__main__':
    executor.start_polling(dp)