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
from datetime import datetime, timedelta


logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# form taskForm
class taskForm(StatesGroup):
    title = State()
    text = State()
    executor = State()
    deadline = State()


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
                  config.OBJECT_TEXT['user']['add_task'],
                  config.OBJECT_TEXT['user']['my_task'])


@dp.message_handler(lambda message: message.text not in [config.OBJECT_TEXT['user']['users'], config.OBJECT_TEXT['user']['add_task'], config.OBJECT_TEXT['user']['my_task']])
async def render_keyboard(message: types.Message):
    """KEYBOARD RENDER AND HELLO"""

    await message.answer(f"{config.OBJECT_TEXT['user']['login']} {message.chat.username}", reply_markup=main_keyboard)
    
    
# ------------ USERS -------------

@dp.message_handler(Text(equals=config.OBJECT_TEXT['user']['users']))
async def function_all_users(message: types.Message):
    """FUNCTION ALL USERS"""
    
    
    with app.app_context():
        users = Users.query.all()
        
    for i in users:
        contact_keybord = types.InlineKeyboardMarkup(
            resize_keyboard=True, selective=True)
        
        with app.app_context():
            tasks = Tasks.query.filter_by(executor=i.id).all()
        
        login_btn = types.InlineKeyboardButton(f'Написать', url=f'https://t.me/{i.login}')
        contact_keybord.add(login_btn)
        
        await bot.send_message(message.chat.id, i.login + '(Список задачь)', reply_markup=contact_keybord, parse_mode=ParseMode.MARKDOWN)
            
        if len(tasks) > 0:
            for task in tasks:
                task_info = task.title + '\n' + task.text + '\n' + 'Deadline: ' + str(task.deadline)
                await bot.send_message(message.chat.id, task_info, parse_mode=ParseMode.MARKDOWN)
        else:
            await bot.send_message(message.chat.id, 'Не занят 😱', parse_mode=ParseMode.MARKDOWN)
                
        
        
        
@dp.message_handler(Text(equals=config.OBJECT_TEXT['user']['my_task']))
async def function_my_task(message: types.Message):
    """FUNCTION MY TASK"""
    
    with app.app_context():
        tasks = Tasks.query.filter_by(executor=message.chat.id).all()
        
    if len(tasks) > 0:
        for task in tasks:
            task_info = task.title + '\n' + task.text + '\n' + 'Deadline: ' + str(task.deadline)
            await bot.send_message(message.chat.id, task_info, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(message.chat.id, 'Пусто 🥹', parse_mode=ParseMode.MARKDOWN)
            
        
        
# ------------ CREATE TASK -------------

@dp.message_handler(Text(equals=config.OBJECT_TEXT['user']['add_task']))
async def function_add_task(message: types.Message):
    """FUNCTION ADD TASK"""
    
    
    await taskForm.title.set()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['task']['enter_title'])
    

@dp.message_handler(state=taskForm.title)
async def process_title(message: types.Message, state: FSMContext):
    """TITLE STATE"""

    async with state.proxy() as data:
        data['title'] = message.text

    # start text state
    await taskForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['task']['enter_text'])
    
def render_user_keyboard():
    keyboard = types.InlineKeyboardMarkup(
    resize_keyboard=True, selective=True)
    for user in Users.query.all():
        btn = types.InlineKeyboardButton(user.login, callback_data=f'executor_{user.login}')
        keyboard.add(btn)
        
    return keyboard

@dp.message_handler(state=taskForm.text)
async def process_text(message: types.Message, state: FSMContext):
    """TEXT STATE"""

    async with state.proxy() as data:
        data['text'] = message.text

    # start text state
    await taskForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['task']['enter_executor'], reply_markup= render_user_keyboard())
    

@dp.callback_query_handler(Text(startswith="executor_"), state=taskForm.executor)
async def callbacks_executor(call: types.CallbackQuery, state: FSMContext):
    action = call.data.split('_')[1]
    
    user =  Users.query.filter_by(login=action).first()
    
    async with state.proxy() as data:
        data['executor'] = user.id
        
    await taskForm.next()
    await bot.send_message(call.message.chat.id, config.OBJECT_TEXT['task']['enter_deadline'])
    
@dp.message_handler(lambda message: not message.text.isdigit(), state=taskForm.deadline)
async def process_deadline_invalid(message: types.Message):
    return await message.reply(config.OBJECT_TEXT['task']['int_exec'])

@dp.message_handler(state=taskForm.deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    """EXECUTOR STATE"""

    async with state.proxy() as data:
        data['deadline'] = datetime.now() + timedelta(days=int(message.text)) 
        
        with app.app_context():
            task = Tasks(title=data['title'],
                         author=message.chat.id,
                         executor=data['executor'],
                         text=data['text'],
                         deadline=data['deadline'])
            
            db.session.add(task)
            db.session.commit()
            
            user = Users.query.filter_by(id=data['executor']).first()
            
            task_info = md.text(
                md.text('Наименование: ', md.bold(data['title'])),
                md.text('Автор: ', md.bold(message.chat.username)),
                md.text('Исполнитель: ', md.bold(user.login)),
                md.text('Текст: ', data['text']),
                md.text('Дедлайн: ', data['deadline']),
                sep='\n',)

            await bot.send_message(message.chat.id, md.text(config.OBJECT_TEXT['task']['finish_add']), parse_mode=ParseMode.MARKDOWN)
            await bot.send_message(message.chat.id, task_info, parse_mode=ParseMode.MARKDOWN)
            
            if message.chat.username != data['executor']:
                await bot.send_message(data['executor'], task_info, parse_mode=ParseMode.MARKDOWN)
            

    # stop state
    await state.finish()
        
        
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)