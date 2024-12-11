from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить задачи Taste'), KeyboardButton(text='Получить задачи Office'), KeyboardButton(text='Получить задачи Idea')],
    [KeyboardButton(text='Получить все задачи')], [KeyboardButton(text='Закрыть задачу')],[KeyboardButton(text='Добавить сотрудника Spot'), KeyboardButton(text='Удалить сотрудника Spot')]
    ], resize_keyboard=True)

no_adm = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌а можно НЕ надо', callback_data='NO')]])
