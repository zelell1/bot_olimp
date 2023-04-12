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
a = []
@dp.message_handler(commands=['start'])  # функция вызова сообщения с помощью
async def helping(message: types.Message):
    global user
    inf_user = message.from_user
    user = User(inf_user['id'], inf_user['first_name'], inf_user['last_name'], inf_user['username'])
    user.add_user()
    keyboard = InlineKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(InlineKeyboardButton(text=f"""Я хочу продолжить""", callback_data="continue"))
    await message.answer(f"""<strong>Это персональный-бот помощник.</strong> 
Он будет помогать вам в отслеживании олимпиад.\t
С ним больше не беспокойтесь, что пропустите олимпиаду.""", parse_mode="HTML", reply_markup=keyboard)
    

@dp.callback_query_handler(text="continue")
async def continu(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.delete()
    usern = user.usernam()
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Отркыть веб страницу', web_app=WebAppInfo(url='https://zelell1.github.io/')))
    await call.message.answer(f"""Приветствую {usern}, теперь пожалуйста выберите предметы, в которые вас интересуют""", parse_mode="HTML", reply_markup=markup)
    

if __name__ == '__main__':
    executor.start_polling(dp)