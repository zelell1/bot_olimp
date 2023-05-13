from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from Token import TOKEN
from aiogram.types.web_app_info import WebAppInfo
from init_db import User, get_users
import requests
import re
import emoji
import asyncio
import datetime
import aioschedule
import requests
import sqlite3


# Создаем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
Users = dict()
usr = get_users()
for i in usr:
    Users[str(i[0])] = User(i[0], i[1], i[2], i[3], '')
    

# функция начинает работу бота
@dp.message_handler(commands=['start'])  
async def starting(message: types.Message):
    inf_user = message.from_user
    user = User(inf_user['id'], inf_user['first_name'], inf_user['last_name'], inf_user['username'], '')
    if str(inf_user['id']) not in Users.keys():
        Users[str(inf_user['id'])] = user
    if user.add_user():
        user.add_user()
        await message.answer(f"""<strong>Это персональный-бот помощник.</strong> 
Он будет помогать вам в отслеживании олимпиад.\t
С ним больше не беспокойтесь, что пропустите олимпиаду.""", parse_mode="HTML")
        await message.answer(f"""Спасибо за регистрацию.""", parse_mode="HTML")
    else:
        await message.answer(f"""Вы уже зарегистрированы.""", parse_mode="HTML")
    

#функция выводит профили олимпиад
@dp.message_handler(commands=['add'])
async def olimpiads(message: types.Message):
    inf_user = message.from_user
    user = Users[str(inf_user['id'])]
    usern = user.usernam()
    url = 'http://127.0.0.1:8000/list_olimpix'
    response = requests.get(url=url).json()
    keyboard = types.InlineKeyboardMarkup()
    for elem in response:
        keyboard.add(types.InlineKeyboardButton(text=elem, callback_data=f"p:{elem}:{response.index(elem)}"))
    await message.answer(f"""Приветствую {usern}, теперь пожалуйста выберите профили предметов, в которые вас интересуют""", parse_mode="HTML", reply_markup=keyboard)
    

# когда пользователь выбрал профиль олимпиады, бот начинает выводить перечневые олимпиады по выбранному профилю
@dp.callback_query_handler(text_startswith="p") 
async def find_in_prof(query: CallbackQuery):
    await query.answer()
    await query.message.delete()
    data = query.data.split(':')
    prof = data[-2]
    ind = int(data[-1])
    url = 'http://127.0.0.1:8000/olimpix'
    response = requests.get(url=url).json()
    await query.message.answer("""Когда будете выбирать олимпиады пожалуйста введите команду /append и введите цифры уникального кода олимпиады""", parse_mode="HTML")
    await query.message.answer("""Например /append 5251 1324 4314 и т.д""", parse_mode="HTML")
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
        

# функция добавляет олимпиады к пользователю
@dp.message_handler(commands=['append'])  
async def appending(message: types.Message):
    try:
        com = "".join(message.get_full_command()[1])
        com = re.findall(r'(?i)([0-9]+)', com)
        url = 'http://127.0.0.1:8000/olimpix'
        data = []
        response = requests.get(url=url).json()
        for i in response:
            for j in i.values():
                for k in j:
                    dataset = k["".join(list(k.keys()))]
                    uniq = dataset[-1].split('/')[-1]
                    if str(uniq) in com:
                        data.append(uniq)
                        del com[com.index(str(uniq))]
        inf_user = message.from_user
        user = Users[str(inf_user['id'])]
        user.update_info_user(data)
        await message.answer(f"""<strong>Вы успешно добавили олимпиады/олимпиаду</strong>""", parse_mode="HTML")
    except Exception:
        await message.answer(f"""<strong>Введен некорректный запрос</strong>""", parse_mode="HTML")


# функция выводит список олимпиад пользователю
@dp.message_handler(commands=['list'])
async def list_olimpiads(message: types.Message):
    inf_user = message.from_user
    user = Users[str(inf_user['id'])]
    lst = user.get_list()
    try:
        if lst == [] or lst == ['']:
            raise Exception
        if lst[0] == '':
            del lst[0]
        url = 'http://127.0.0.1:8000/list'
        response = requests.get(url=url).json()
        a = []
        for i in response:
            dictt = {}
            for key, val in i.items():
                names = []
                for j in val:
                    if j[0] in lst:
                        names.append(j[1])
                        del lst[lst.index(j[0])]
                if names != []:
                    dictt[key] = names
            if dictt != {}:
                a.append(dictt)
        for i in a:
            for key, val in i.items():
                await message.answer(f"""<strong>{key}</strong>""", parse_mode="HTML")
                await message.answer('\n'.join(list(map(lambda x: emoji.emojize(':large_orange_diamond:') + x, val))))
    except Exception:
        await message.answer(f"""<strong>Пока что вы не добавили ни одной олимпиады</strong>""", parse_mode="HTML")


#функция анализирует новости по времени
@dp.message_handler()
async def choose_your_dinner():
    # inf_user = message.from_user
    # user = Users[str(inf_user['id'])]
    for key, val in Users.items():
        lst = val.get_list()
        try:
            if lst == [] or lst == ['']:
                raise Exception
            if lst[0] == '':
                del lst[0]
            time = datetime.datetime.now()
            for i in lst:
                url = f'http://127.0.0.1:8000/news/{i}'
                response = requests.get(url=url).json()
                tm = response[0]
                date = int(tm[0])
                month = int(tm[1])
                year = int(tm[2])
                # для демонтстрации
                # date = time.day
                # month = time.month
                # year = time.year
                print(time.year, time.day, time.month)
                if int(time.year) == year and int(time.day) == date and int(time.month) == month:
                    await bot.send_message(chat_id=int(key), text=f"""<strong>Новость по олимпиаде {response[-1]}</strong>""", parse_mode="HTML")
                    await bot.send_message(chat_id=int(key), text=f"""{response[1]}""", parse_mode="HTML")
        except Exception:
            pass


# функция которая в определенное время выводит новости пользователю
async def scheduler():
    aioschedule.every().day.at("17:00").do(choose_your_dinner)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
        
async def on_startup(dp): 
    asyncio.create_task(scheduler())

    
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    