import requests
from bs4 import BeautifulSoup
import schedule
import time
import asyncio
import itertools
from app.database.requests import insert_order_in_db , get_all_orders
#from app.handlers import process_order

#url = 'https://freelance.habr.com/tasks?q=tg+b'
url = 'https://freelance.habr.com/tasks'

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')



async def parsing (soup,message) :
    # получение 1 заказа с сайта
    for card in soup.find_all('li', class_ = 'content-list__item'): #получение 1 заказа с сайта
        order_name = card.find('div', class_ = 'task__title').text.strip()
        if card.find('span', class_ = 'count') is not None:
            order_price =card.find('span', class_ = 'count').text
        else:
            order_price ='Договорная'
        order_link_tag = card.find('a', class_='')  # Находим тег <a>
        order_link = order_link_tag.get('href')  # Извлекаем значение атрибута href
        description = "This is a sample description"

        #алгоритм проверки на присутствие его в БД
        all_orders = await get_all_orders()
        all_orders_list = list(all_orders)

        # Переворачиваем список, чтобы получить последние 50 заказов
        reversed_orders = reversed(all_orders_list)
        i = 0;
        for order in itertools.islice(reversed_orders,50):
            if order_link == order.link:
                print('Про'+ order_link + ' Вы уже знаете!')
                i=1;
                break;
        if i!=1:
            print('Попался уникальный заказ! '+ order_name)
            await insert_order_in_db(order_name, str(order_price), order_link, description)
            await message.answer(
                f"Новый заказ:\nНазвание: {order_name}\nЦена: {order_price}\nСсылка: https://freelance.habr.com{order_link}\nОписание: {description}")

        #print('title -> ' + order_name)
        #print('price -> ' + str(order_price))
        #print('link -> '+'https://freelance.habr.com'+order_link)
        #print('_____________________________')

#async def print_order():
  #  return ([order_name,str(order_price),order_link,description])

async def start_parser(message):
    await parsing(soup, message)
    #await asyncio.sleep(1)  # Задержка на 30 секунд

async def stop_parser(stop_event):
    stop_event.set()


# Запуск асинхронной функции
#asyncio.run(main_parser())