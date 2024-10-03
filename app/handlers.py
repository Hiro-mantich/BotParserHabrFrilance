from aiogram import F , Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InputFile,BufferedInputFile
import os
import asyncio

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pyexpat.errors import messages

import app.keyboards as kb
import app.database.requests as rq

from parserHabrFrilance import start_parser, stop_parser

import app.database.requests as rq

router = Router()

@router.message(CommandStart()) #Команда старт
async def cmd_start(message:Message):
    tg_id = message.from_user.id
    user = await rq.get_user_tg_id(tg_id)
    if user:
        await message.reply(f"Приветствую, друг мой, {user.login}",
                            reply_markup=kb.btns_main_menu)
    else:
        await message.reply('Кто ты, чужак?',
                            reply_markup=kb.btns_auth_menu)

@router.message(F.text == 'GO!')
async def start_parsing(message:Message):
    await message.answer('Start parsing for orders')
    while True:
        await start_parser(message)
        await asyncio.sleep(120)
    #await message.answer('Больше заказов пока нет.')


@router.message(F.text == 'Stop')
async def stop_parsing(message:Message):
      #stop_event.set()
      await message.answer('Stop parsing for orders')

class LogInForm(StatesGroup): #клас авторизации
    entering_login = State()
    entering_password = State()

@router.message(F.text == 'Log in')
async def log_in(message: Message, state: FSMContext):
    await message.answer('Для авторизации тебе необходимо ввести логин и пароль.\nВведи логин ->')

    await state.set_state(LogInForm.entering_login)

@router.message(LogInForm.entering_login)
async def log_in_login(message: Message, state: FSMContext):
    login = message.text
    await state.update_data(login = login)
    if await rq.get_user(login) is not None:
        user = await rq.get_user(login)
        await message.answer("Тот ли ты, за кого себя выдаёшь? Подтверди это ПАРОЛЕМ!")
        #await message.answer('Введи пароль ->')
        await state.set_state(LogInForm.entering_password)
    else:
        await message.answer("Я таких не знаю! Упёрдывай, приблуда!")
        await state.clear()


@router.message(LogInForm.entering_password)
async def log_in_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    login = user_data.get('login')
    password = message.text
    tg_id = message.from_user.id
    await rq.set_user_tg_id(login,tg_id)


    await message.answer(f'Авторизация завершена!',
                         reply_markup=kb.btns_main_menu)
    await state.clear()


class SignInForm(StatesGroup):
    entering_login = State()
    entering_password = State()

@router.message(F.text == 'Sign in')
async def sign_in(message: Message, state: FSMContext):
    await message.answer('Для регистрации тебе необходими придумать логин и пароль (до 10 символов).\nВведи логин ->')
    await state.set_state(SignInForm.entering_login)

@router.message(SignInForm.entering_login)
async def enter_login(message: Message, state: FSMContext):
    login = message.text
    await state.update_data(login=login)
    await message.answer('Введи пароль ->')
    await state.set_state(SignInForm.entering_password)


@router.message(SignInForm.entering_password)
async def enter_password(message: Message, state: FSMContext):
    login = await state.get_data() #получею все данные
    user_login = login.get('login') # из всех данных получаю логин

    user_password = message.text #получаю из сообщения пользователя пароль
    tg_user_id = message.from_user.id #получаю id пользователя
    user_name = message.from_user.full_name

    await rq.sign_in_user(tg_user_id,user_login,user_password)

    await message.answer(f'Регистрация завершена!\n'
                     f'Твоё имя в ТГ: {user_name}\nТвой id: {tg_user_id}\nЛогин: {user_login}\nПароль: {user_password} ',
                            reply_markup=kb.btns_main_menu)
    await state.clear()

@router.message(F.text == 'Log out')
async def log_out(message: Message):
    tg_id = message.from_user.id
    await rq.log_out(tg_id)
    await message.answer('Вы разлогинились.',
                            reply_markup=kb.btns_auth_menu)