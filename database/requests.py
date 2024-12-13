from database.models import async_session
from database.models import User, Task
from sqlalchemy import select, and_
import admin.requests_admin as rq_adm
from bot_file import bot

async def add_task(tg_id, task, deadline, type_task):
    async with async_session() as session:
        session.add(Task(tg_id=tg_id, task=task, deadline=deadline, status=False, type_task=type_task))
        admins = await rq_adm.get_all_admin()
        for admin in admins:
            try:
                if deadline == '':
                    await bot.send_message(admin.tg_id, f'Добавлена задача от сотрудника: {await rq_adm.check_name(tg_id)}\n\nЗадача: {task}\nТип задачи: {type_task}')
                else:
                    await bot.send_message(admin.tg_id, f'Добавлена задача от сотрудника: {await rq_adm.check_name(tg_id)}\n\nЗадача: {task}\nТип задачи: {type_task}\nDeadline: {deadline}')
            except Exception as e:
                print(f"Error: {e}")
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