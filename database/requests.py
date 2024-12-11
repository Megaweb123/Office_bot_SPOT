from database.models import async_session
from database.models import User, Task
from sqlalchemy import select, and_

async def add_task(tg_id, task, deadline, type_task):
    async with async_session() as session:
        session.add(Task(tg_id=tg_id, task=task, deadline=deadline, status=False, type_task=type_task))
        await session.commit()

async def check_user(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        if not user:
            return False
        else:
            return True

async def check_user_is_adm(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(and_(User.tg_id == user_id, User.is_admin == True)))
        if not user:
            return False
        else:
            return True

async def get_all_my_tasks(id):
    async with async_session() as session:
        tasks = select(Task).where(and_(Task.tg_id == id, Task.status == False))
        result = await session.execute(tasks)
        all_task = result.scalars().all()
        return all_task