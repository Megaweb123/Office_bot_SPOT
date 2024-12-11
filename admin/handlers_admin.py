from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import datetime

import admin.keyboards_admin as kb_adm
import admin.requests_admin as rq_adm
import database.requests as rq

from bot_file import bot
router_adm = Router()
    
class ClosedTask(StatesGroup):
    task_id = State()
    message = State()
    message_standart = State()
    user_tg_id = State()

class AddUser(StatesGroup):
    tg_id = State()
    name = State()
    birthday = State()

class DelUser(StatesGroup):
    tg_id = State()
    
@router_adm.message(Command('admin'))
async def admin(message:Message):
    is_admin = await rq.check_user_is_adm(message.chat.id)
    if is_admin:
        await message.answer('Клавиатура для админа открыта', reply_markup=kb_adm.main_admin)

@router_adm.message(F.text == 'Получить все задачи')
async def take_all_task(message: Message):
    is_admin = await rq.check_user_is_adm(message.chat.id)
    if is_admin:
        tasks = await rq_adm.check_all_tasks()
        if len(tasks) == 0:
            await message.answer('Задач нет, можно спать!')
        else:
            for task in tasks:
                text = f'Номер задачи: {task.id}\nЗадача: {task.task}\nТип задачи: {task.type_task}'
                if task.deadline != '':
                    text += f'\nDeadline: {task.deadline}'
                await message.answer(text)


@router_adm.message(F.text == 'Получить задачи Taste')
async def take_taste_task(message: Message):
    is_admin = await rq.check_user_is_adm(message.chat.id)
    if is_admin:
        await message.answer('Проверяю наличие задач..')
        tasks = await rq_adm.check_tasks('taste')
        if len(tasks) == 0:
            await message.answer('Запросов на вкусняшки нет, какие задачи получить?')
        else:
            for task in tasks:
                text = f'Номер задачи: {task.id}\nЗадача: {task.task}\nТип задачи: {task.type_task}'
                await message.answer(text)

@router_adm.message(F.text == 'Получить задачи Office')
async def take_studio_task(message: Message):
    is_admin = await rq.check_user_is_adm(message.chat.id)
    if is_admin:
        await message.answer('Проверяю наличие задач..')
        tasks = await rq_adm.check_tasks('office')
        if len(tasks) == 0:
            await message.answer('Запросов для офиса нет')
        else:
            for task in tasks:
                text = f'Номер задачи: {task.id}\nЗадача: {task.task}\nТип задачи: {task.type_task}\nDeadline: {task.deadline}'
                await message.answer(text)

@router_adm.message(F.text == 'Получить задачи Idea')
async def take_idea_task(message: Message):
    is_admin = await rq.check_user_is_adm(message.chat.id)
    if is_admin:
        await message.answer('Проверяю наличие задач..')
        tasks = await rq_adm.check_tasks('idea')
        if len(tasks) == 0:
            await message.answer('Идей/запросов ни у кого нет')
        else:
            for task in tasks:
                text = f'Номер задачи: {task.id}\nЗадача: {task.task}\nТип задачи: {task.type_task}\nDeadline: {task.deadline}'
                await message.answer(text)

@router_adm.message(F.text == 'Закрыть задачу')
async def closed_task_start(message: Message, state: FSMContext):
    is_admin = await rq.check_user_is_adm(message.chat.id)
    if is_admin:
        await state.set_state(ClosedTask.task_id)
        await message.answer('Введите номер задачи')

@router_adm.message(ClosedTask.task_id)
async def closed_task_id(message: Message, state: FSMContext):
    is_admin = await rq.check_user_is_adm(message.chat.id)
    if is_admin:
        try:
            id = int(message.text)
            result = await rq_adm.check_task(id)
            if len(result) == 2:
                await message.answer(result[0])
                try:
                    await state.update_data(tg_id=result[1])
                    await state.update_data(message_standart=result[0])
                    await state.set_state(ClosedTask.message)
                    await message.answer('Написать сообщение сотруднику, оставившему эту задачу?', reply_markup=kb_adm.no_adm)
                except:
                    print('Не получилось отправить сообщение')
            else:
                await message.answer(result)
                await state.clear()
        except:
            await message.answer('Номер задачи некорректный')
            await state.clear()

@router_adm.message(ClosedTask.message)
async def closed_task_message(message: Message, state: FSMContext):
    print('НЕ NO')
    closed_task = await state.get_data()
    await bot.send_message(closed_task['tg_id'], closed_task['message_standart'])
    await bot.send_message(closed_task['tg_id'], message.text)
    await state.clear()

@router_adm.callback_query(ClosedTask.message)
async def closed_task_callback(callback: CallbackQuery, state: FSMContext):
    print('NO')
    await callback.answer()
    closed_task = await state.get_data()
    await bot.send_message(closed_task['tg_id'], closed_task['message_standart'])
    await state.clear()

@router_adm.message(F.text == 'Добавить сотрудника Spot')
async def add_user(message: Message, state: FSMContext):
    is_admin = await rq.check_user_is_adm(message.chat.id)
    if is_admin:
        await state.set_state(AddUser.tg_id)
        await message.answer('Укажите telegram_id сотрудника Spot')

@router_adm.message(AddUser.tg_id)
async def add_user_step_tg_id(message: Message, state: FSMContext):
    check = await rq.check_user(int(message.text))
    if check:
        await message.answer('Сотрудник Spot с таким id уже есть')
        await state.clear()
    else:
        await state.update_data(tg_id=int(message.text))
        await state.set_state(AddUser.name)
        await message.answer('Укажите фамилию и имя сотрудника')

@router_adm.message(AddUser.name)
async def add_user_step_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddUser.birthday)
    await message.answer('Укажите дату рождения сотрудника\nФормат: yyyy.mm.dd')

@router_adm.message(AddUser.birthday)
async def add_user_step_name(message: Message, state: FSMContext):
    try:
        birthday = datetime.strptime(message.text, '%Y.%m.%d').date()
        await state.update_data(birthday=birthday)
        user_data = await state.get_data()
        await message.answer('Записываю...')
        await rq_adm.added_user(user_data['tg_id'], user_data['name'], birthday)
        await message.answer('Записал')
        await state.clear()
    except ValueError as er:
        print(er)
        await message.answer('Записать не получилось :c\nПроверьте формат ввода даты рождения.')
        await state.clear()

@router_adm.message(F.text == 'Удалить сотрудника Spot')
async def del_user(message: Message, state: FSMContext):
    is_admin = await rq.check_user_is_adm(message.chat.id)
    if is_admin:
        await state.set_state(DelUser.tg_id)
        await message.answer('Укажите telegram_id (уже бывшего) сотрудника Spot')

@router_adm.message(DelUser.tg_id)
async def del_user_step_tg_id(message: Message, state: FSMContext):
    try:
        check = await rq.check_user(int(message.text))
        if check:
            user = await rq_adm.delete_user(int(message.text))
            await message.answer(f'Сотрудник Spot {user} c telegram_id: "{message.text}" удален')
            await state.clear()
        else:
            await message.answer('Сотрудника Spot с таким id нет')
            await state.clear()
    except ValueError as er:
        await state.clear()
        await message.answer(f'Ошибка:{er}\nПроверьте правильность введения telegram_id')