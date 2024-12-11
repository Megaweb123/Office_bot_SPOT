from database.models import async_session
from database.models import User, Task
from sqlalchemy import select, delete, and_



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