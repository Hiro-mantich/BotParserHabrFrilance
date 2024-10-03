from app.database.models import async_session
from app.database.models import Order
from app.database.models import User
from sqlalchemy import select

async def insert_order_in_db(title_order,price_order,link_order,description_order):
    async with async_session() as session:
        async with session.begin():
            # Создаем экземпляр Order и заполняем его поля
            new_order = Order(
                title=title_order,
                price=price_order,
                link=link_order,
                description="This is a sample description"
            )
            # Добавляем экземпляр в сессию
            session.add(new_order)
            # Транзакция будет зафиксирована автоматически при выходе из блока `async with session.begin()`

async def log_out(tg_id):
    async with async_session() as session:
        await session.scalar(select(User).where(User.tg_id ==tg_id ))
        User.tg_id = None
        await session.commit()

async def get_all_orders():
    async with async_session() as session:
        return await session.scalars(select(Order))

async def sign_in_user(tg_user_id,user_login,user_password):
    async with async_session() as session:
        async with session.begin():
            # Создаем экземпляр Order и заполняем его поля
            new_user = User(
                tg_id=tg_user_id,
                login = user_login,
                password=user_password
            )
            # Добавляем экземпляр в сессию
            session.add(new_user)
            await session.commit()
            # Транзакция будет зафиксирована автоматически при выходе из блока `async with session.begin()`

async def get_user_tg_id(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id ))

