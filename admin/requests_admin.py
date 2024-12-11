from database.models import async_session
from database.models import User, Task
from sqlalchemy import select, delete, and_, extract
from datetime import datetime, timedelta, date


async def check_tasks(type_task):
    async with async_session() as session:
        result = await session.execute(select(Task).where(and_(Task.type_task==type_task, Task.status==False)))
        tasks = result.scalars().all()
        return tasks

async def check_all_tasks():
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.status == False))
        tasks = result.scalars().all()
        return tasks

async def check_task(task_id):
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first() 
        tg_id = task.tg_id
        if task is None:
            return f'Такой задачи в базе данных нет'
        if not task.status: 
            task.status = True  
            await session.commit() 
            text = [f'Задача {task_id} закрыта!', tg_id]
            return text
        else: 
            return f'Задача {task_id} закрыта ранее!'

async def added_user(tg_id, name, birthday):
    async with async_session() as session:
        session.add(User(tg_id=tg_id, name_and_lastname=name, birthday=birthday))
        await session.commit()

async def delete_user(tg_id):
    async with async_session() as session:
        user_to_delete = select(User.name_and_lastname).where(User.tg_id == tg_id)
        user_for_del = delete(User).where(User.tg_id == tg_id)
        result = await session.execute(user_to_delete)
        result = result.scalar()
        await session.execute(user_for_del)
        await session.commit()
        return result
    
async def check_name(tg_id):
    async with async_session() as session:
        request = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(request)
        return user.name_and_lastname

async def get_all_users():
    async with async_session() as session:
        request = await session.execute(select(User))
        users = request.scalars().all()
        return users

async def get_all_admin():
    async with async_session() as session:
        request = await session.execute(select(User).where(User.is_admin==True))
        users = request.scalars().all()
        return users

async def check_birthday():
    async with async_session() as session:
        two_weeks_later = date.today() + timedelta(days=15)
        current_month = two_weeks_later.month
        current_day = two_weeks_later.day
        request = await session.execute(select(User).where(and_(extract('month', User.birthday) == current_month, extract('day', User.birthday) == current_day)))
        users = request.scalars().all()
        return users