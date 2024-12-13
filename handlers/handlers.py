from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

import handlers.keyboards as kb
import database.requests as rq
router = Router()


class AddedTask(StatesGroup):
    task = State()
    deadline = State()

class AddedTeste(StatesGroup):
    task = State()

class AddedOffice(StatesGroup):
    tg_id = State()
    task = State()
    deadline = State()

@router.callback_query(F.data == 'stop_write')
async def back_button(callback: CallbackQuery, state: FSMContext):
    if await rq.check_user(callback.from_user.id):
        await callback.answer()
        await state.clear()
        await callback.message.edit_text('Упс! Попробуй еще. Нужно выбрать годную команду.')

@router.message(CommandStart())
async def cmd_start(message: Message):
    if await rq.check_user(message.from_user.id) is True:
        if message.chat.type == 'private':
            await message.answer('Привет, гайз!💅\nЭто бот-ассистент офис-менеджера Spot Film\n'
                            'Я помогаю получать и обрабатывать все ваши запросы, чтобы мы ничего не потеряли и не упустили⚡️', reply_markup=kb.main)
        else:
            await message.answer('Привет, гайз!💅\nЭто бот-ассистент офис-менеджера Spot Film\n'
                            'Я помогаю получать и обрабатывать все ваши запросы, чтобы мы ничего не потеряли и не упустили⚡️')
    else:
        await message.answer('К сожалению, тебя нет в списке ☹\nДля записи - обратись к офис менеджеру')

@router.message(AddedTeste.task)
async def taste_end(message: Message, state: FSMContext):
    if message.text not in ['Spot the Taste😋','Spot the Studio✏', 'Spot the new idea💡']:
        await state.update_data(task=message.text)
        await rq.add_task(tg_id=message.chat.id, task=message.text, deadline='', type_task='taste')
        await message.answer('Cпасибо, твое пожелание как минимум зарегано🤌\nПришлем по апдейтам инфу еще))\nПусть всем будет вкусно!')
        await state.clear()
    else:
        await message.answer('Упс! Попробуй еще. Нужно выбрать годную команду.')
        await state.clear()

@router.message(AddedOffice.task)
async def studio_task(message: Message, state: FSMContext):
    if message.text not in ['Spot the Taste😋', 'Spot the Studio✏', 'Spot the new idea💡']:
        await state.update_data(tg_id=message.from_user.id)
        await state.update_data(task=message.text)
        await state.set_state(AddedOffice.deadline)
        await message.answer('Когда надо?\n[Ответ ""вчера"" принимается в очень исключительных случаях))]', reply_markup=kb.keyboard_deadline)
    else:
        await message.answer('Упс! Попробуй еще. Нужно выбрать годную команду.')
        await state.clear()

@router.callback_query(AddedOffice.deadline)
async def studio_end(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'stop_write':
        await callback.answer('')
        await state.clear()
        await back_button(callback)
    else:
        await callback.answer()
        deadline = (datetime.now() + timedelta(days=int(callback.data))).strftime("%d.%m.%Y")
        data = await state.get_data()
        tg_id = data.get("tg_id")
        task = data.get("task") 
        await rq.add_task(tg_id=int(tg_id), task=task, deadline=deadline, type_task='office')
        await callback.message.edit_text(f'Задача {task} записана\nПланируемая дата выполнения: до {deadline}\nСпасибо!')
        await state.clear()

@router.message(AddedTask.task)
async def idea_task(message: Message, state: FSMContext):
    if message.text not in ['Spot the Taste😋', 'Spot the Studio✏', 'Spot the new idea💡']:
        await state.update_data(tg_id=message.from_user.id)
        await state.update_data(task=message.text)
        await state.set_state(AddedTask.deadline)
        await message.answer('Выбери срок выполнения', reply_markup=kb.keyboard_deadline)
    else:
        await message.answer('Упс! Попробуй еще. Нужно выбрать годную команду.')
        await state.clear()

@router.callback_query(AddedTask.deadline)
async def idea_end(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'stop_write':
        await callback.answer('')
        await state.clear()
        await back_button(callback)
    else:
        await callback.answer()
        deadline = (datetime.now() + timedelta(days=int(callback.data))).strftime("%d.%m.%Y")
        data = await state.get_data()
        tg_id = data.get("tg_id")
        task = data.get("task") 
        await rq.add_task(tg_id=int(tg_id), task=task, deadline=deadline, type_task='idea')
        await callback.message.edit_text(f'Задача {task} записана\nПланируемая дата выполнения: до {deadline}\nСпасибо!')
        await state.clear()

@router.message(F.text == 'Spot the Taste😋')
async def tastе_start(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id) and message.chat.type == 'private':
        await state.set_state(AddedTeste.task)
        await message.answer('Чо по еде?\nВведите что хжелаете заказать из еды или напитков.\nЕсли приложите ссылки +100500 к карме✨', reply_markup=kb.back)

@router.message(F.text == 'Spot the Studio✏')
async def studio_start(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id) and message.chat.type == 'private':
        await state.set_state(AddedOffice.task)
        await message.answer('Смотрим ништяки для офиса, например, бумага или  картриджи, а мб вообще турник?\nПишите чо нужно🧐\n\n[те кто прикладывает ссылки, мои самые лутшие)))]', 
                            reply_markup=kb.back)

@router.message(F.text == 'Spot the new idea💡')
async def idea_start(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id) and message.chat.type == 'private':
        await state.set_state(AddedTask.task)
        await message.answer('Мы рады любому креативу (почти!)\nВозможно нам нужен новый формат мероприятий? А мб съездить всей командой на глэмпинг? А мб сходить на лекцию?\n'
                            'В общем пиши всио: свои идею/задачу или вопрос))', reply_markup=kb.back)

@router.message(F.text == 'Вспомнить всё📝')
async def get_all_tasks(message: Message):
    if await rq.check_user(message.from_user.id) and message.chat.type == 'private':
        tasks = await rq.get_all_my_tasks(int(message.chat.id))
        if len(tasks) == 0:
            await message.answer('От тебя чота пока ничо не прилетало🥲 (и слава богу!)')
        else:
            for task in tasks:
                await message.answer(f'Номер задачи: {task.id}\nЗадача: {task.task}\nСтатус: В работе')

@router.message(F.text == 'Куда заносить кэш ? 🧐')
async def cash(message: Message):
    if await rq.check_user(message.from_user.id) and message.chat.type == 'private':
        await message.answer('Штош...\nПеревести кэш можно по номеру 8925 132 23 31 (на Райф или ВТБ) получатель Диана Владиславовна Ч.\n'
                        'Обязательно просим подписывать для чего перевод или кидать Ди в личку документ перевода и подписать чо каво))\n'
                        'Спасибо!')