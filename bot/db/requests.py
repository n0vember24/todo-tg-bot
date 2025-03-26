from sqlalchemy import select
from sqlalchemy.engine.result import ScalarResult

from bot.db.models import User, Task
from bot.db.models import async_session


async def create_user(tg_id: int) -> None:
	async with async_session() as session:
		user = await session.scalar(select(User).where(User.tg_id == tg_id))
		if not user:
			session.add(User(tg_id=tg_id))
			await session.commit()


async def get_tasks(user_id: int) -> ScalarResult[Task]:
	async with async_session() as session:
		return await session.scalars(select(Task).where(Task.user_id == user_id))


async def get_task(task_id: int) -> Task:
	async with async_session() as session:
		return await session.scalar(select(Task).where(Task.id == task_id))


async def create_task(title: str, description: str, user_id: int) -> None:
	async with async_session() as session:
		task = Task(title=title, description=description, user_id=user_id)
		session.add(task)
		await session.commit()


async def change_task_stat(task_id: int) -> None:
	async with async_session() as session:
		task = await session.scalar(select(Task).where(Task.id == task_id))
		task.is_done = not task.is_done
		await session.commit()


async def delete_task(task_id: int) -> None:
	async with async_session() as session:
		await session.delete(await session.scalar(select(Task).where(Task.id == task_id)))
		await session.commit()


async def update_task(task_id: int, title: str, description: str) -> None:
	async with async_session() as session:
		task = await session.scalar(select(Task).where(Task.id == task_id))
		task.title = title
		task.description = description
		await session.commit()
