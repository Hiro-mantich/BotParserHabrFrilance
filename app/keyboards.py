from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import  ReplyKeyboardBuilder, InlineKeyboardBuilder

btns_auth_menu = ReplyKeyboardMarkup(keyboard =[
    [KeyboardButton(text ='Log in')],
    [KeyboardButton(text ='Sign in')],
    [KeyboardButton(text ='About')]],
        resize_keyboard = True,
        input_field_placefolder = 'Выберите действие')

btns_main_menu = ReplyKeyboardMarkup(keyboard =[
    [KeyboardButton(text ='GO!')],
    [KeyboardButton(text ='Stop')],
    [KeyboardButton(text ='About')],
    [KeyboardButton(text ='Log out')]],
        resize_keyboard = True,
        input_field_placefolder = 'Выберите действие')


async def btn_main_menu():
    keyboard = ReplyKeyboardBuilder()
    for btn in btns_main_menu:
        keyboard.add(KeyboardButton(text=btn))
    return keyboard.adjust(2).as_markup()

async def btn_auth_menu():
    keyboard = ReplyKeyboardBuilder()
    for btn in btns_auth_menu:
        keyboard.add(KeyboardButton(text=btn))
    return keyboard.adjust(2).as_markup()

