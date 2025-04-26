from datetime import datetime

from sqlalchemy import Integer, BigInteger, DateTime, String, Boolean, ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from bot.config import DB_ENGINE

engine = create_async_engine(url=DB_ENGINE)
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Base model
class Base(AsyncAttrs, DeclarativeBase):
	"""Base class for models"""


class User(Base):
	__tablename__ = 'users'
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	tg_id: Mapped[BigInteger] = mapped_column(BigInteger, unique=True, nullable=False)
	join_date: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
	tasks: Mapped[list['Task']] = relationship(back_populates='user', cascade='all, delete')


class Task(Base):
	__tablename__ = 'tasks'
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	title: Mapped[str] = mapped_column(String(50), nullable=False)
	description: Mapped[str] = mapped_column(String(200))
	is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
	user_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey('users.id'))
	user: Mapped[User] = relationship(back_populates='tasks')


# Main function to create database structure
async def async_main():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
