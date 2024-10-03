import sqlalchemy
from sqlalchemy import BigInteger, String,LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped , mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs,async_sessionmaker, create_async_engine



engine = create_async_engine(url='sqlite+aiosqlite:///db_order.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs,DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25))
    price: Mapped[str] = mapped_column(String(25))
    link: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(100))

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column()
    login: Mapped[str] = mapped_column(String(10))
    password: Mapped[str] = mapped_column(String(10))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)