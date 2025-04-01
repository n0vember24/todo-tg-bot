import logging
from typing import Optional

from sqlalchemy import select, func

from bot.db.models import User, Task, async_session


class UserManager:
	"""Class is designed to work with specidif and all users in database"""

	def __init__(self, user_id: int = None):
		self.user_id = user_id

	@staticmethod
	async def get_by_id(user_id: int) -> Optional[User]:
		"""Get user from database by id"""
		try:
			if user_id:
				async with async_session() as session:
					return await session.scalar(select(User).where(User.id == user_id))
			else:
				raise ValueError('user_id is required')
		except Exception as e:
			logging.error('DB: error in getting user by ID: %s', e)
			return None

	async def create(self) -> None:
		"""Create a new user in database if it does not exist"""
		try:
			if self.user_id:
				async with async_session() as session:
					user = await session.scalar(select(User).where(User.tg_id == self.user_id))
					if not user:
						new_user = User(tg_id=self.user_id)
						session.add(new_user)
						await session.flush()
						await session.commit()
			else:
				raise ValueError('user_id is required')
		except Exception as e:
			logging.error('DB: error in creating new user: %s', e)

	@staticmethod
	async def get() -> list[User]:
		"""Get all users from database"""
		try:
			async with async_session() as session:
				return list(await session.scalars(select(User)))
		except Exception as e:
			logging.error('DB: error in getting users: %s', e)
			return []

	@staticmethod
	async def count() -> int:
		"""Get count of all users in database"""
		try:
			async with async_session() as session:
				return await session.scalar(select(func.count()).select_from(User))
		except Exception as e:
			logging.error('DB: error in getting users count: %s', e)
			return 0


class TaskManager:
	"""Class is designed to work with certain and all tasks in database"""

	def __init__(self, user_id: int = None, title: str = None, description: str = None, task_id: int = None):
		self.user_id = user_id
		self.title = title
		self.description = description
		self.task_id = task_id

	@staticmethod
	async def get(task_id: int) -> Optional[Task]:
		"""Get task by its :code:`id`"""
		try:
			async with async_session() as session:
				return await session.scalar(select(Task).where(Task.id == task_id))
		except Exception as e:
			logging.error('DB: error in getting task by id: %s', e)
			return None

	@staticmethod
	async def get_by_user(user_id: int) -> list[Task]:
		"""Get all tasks for specific user by :code:`user_id`"""
		try:
			async with async_session() as session:
				return list(await session.scalars(select(Task).where(Task.user_id == user_id)))
		except Exception as e:
			logging.error('DB: error in getting tasks by user id: %s', e)
			return []

	@staticmethod
	async def count(user_id: Optional[int] = None) -> int:
		"""Get count of all tasks or for specific user, :code:`user_id` is optional"""
		try:
			if user_id:
				async with async_session() as session:
					return await session.scalar(select(func.count()).select_from(Task).where(Task.user_id == user_id))
			else:
				async with async_session() as session:
					return await session.scalar(select(func.count()).select_from(Task))
		except Exception as e:
			logging.error('DB: error in getting tasks count: %s', e)
			return 0

	async def create(self) -> None:
		"""Create a new task by using given parameters"""
		try:
			async with async_session() as session:
				new_task = Task(title=self.title, description=self.description, user_id=self.user_id)
				session.add(new_task)
				await session.flush()
				await session.commit()
		except Exception as e:
			logging.error('DB: error in creating new task: %s', e)

	async def update(self) -> None:
		"""Update task by using given parameters"""
		try:
			async with async_session() as session:
				task = await session.scalar(select(Task).where(Task.id == self.task_id))
				if task:
					task.title = self.title
					task.description = self.description
					await session.commit()
		except Exception as e:
			logging.error('DB: error in updating task: %s', e)

	async def delete(self) -> None:
		"""Delete task by its :code:`id`"""
		try:
			if self.task_id:
				async with async_session() as session:
					task = await session.scalar(select(Task).where(Task.id == self.task_id))
					if task:
						await session.delete(task)
						await session.commit()
			else:
				raise ValueError('task_id is required')
		except Exception as e:
			logging.error('DB: error in deleting task: %s', e)

	async def toggle_status(self) -> None:
		"""Toggle task status by its :code:`id`"""
		try:
			if self.task_id:
				async with async_session() as session:
					task = await session.scalar(select(Task).where(Task.id == self.task_id))
					if task:
						task.is_done = not task.is_done
						await session.commit()
			else:
				raise ValueError('task_id is required')
		except Exception as e:
			logging.error('DB: error in changing task status: %s', e)
