from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import config
from db import db, Users, app, Tasks
from aiogram.types import ParseMode
from aiogram.utils.markdown import link
import logging
import aiogram.utils.markdown as md
import datetime


logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """START HANDLING"""
    
    with app.app_context():
        # save USER data in db
        try:
            user = Users(
                id=str(message.chat.id),
                login=message.chat.username)

            db.session.add(user)
            db.session.commit()
            
            await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['finish_registration'])
            await bot.send_message(message.chat.id, f"{config.OBJECT_TEXT['user']['login']} {message.chat.username}")
            
        except Exception as e:
            print(e)
            await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['no_login'])
            

# main keyboard
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.row(config.OBJECT_TEXT['user']['users'],
                  config.OBJECT_TEXT['user']['add_task'])


@dp.message_handler(lambda message: message.text not in [config.OBJECT_TEXT['user']['users']])
async def render_keyboard(message: types.Message):
    """KEYBOARD RENDER AND HELLO"""

    await message.answer(f"{config.OBJECT_TEXT['user']['login']} {message.chat.username}", reply_markup=main_keyboard)
    
    
# ------------ USERS -------------

@dp.message_handler(Text(equals=config.OBJECT_TEXT['user']['users']))
async def function_my_objects(message: types.Message):
    """FUNCTION MY OBJECTS"""
    
    
    with app.app_context():
        object = Users.query.all()
        
    for i in object:
        contact_keybord = types.InlineKeyboardMarkup(
            resize_keyboard=True, selective=True)
        
        with app.app_context():
            tasks = Tasks.query.filter_by(executor=i.login).all()
            
        if len(tasks) > 0:
            for task in tasks:
                task_info = task.title + '\n' + task.text + '\n' + 'Deadline: ' + str(task.deadline)
                await bot.send_message(message.chat.id, task_info, parse_mode=ParseMode.MARKDOWN)
        else:
            await bot.send_message(message.chat.id, 'Не занят 😱', parse_mode=ParseMode.MARKDOWN)
                
        login_btn = types.InlineKeyboardButton(f'Написать', url=f'https://t.me/{i.login}')
        contact_keybord.add(login_btn)
        
        await bot.send_message(message.chat.id, i.login, reply_markup=contact_keybord, parse_mode=ParseMode.MARKDOWN)
        
        
        
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)