from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Spot the Taste😋'), KeyboardButton(text='Spot the Studio✏'), KeyboardButton(text='Spot the new idea💡')],
    [KeyboardButton(text='Вспомнить всё📝'), KeyboardButton(text='Куда заносить кэш ? 🧐')]], resize_keyboard=True)

keyboard_deadline = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Неделя', callback_data='7'),
    InlineKeyboardButton(text='Две недели', callback_data='14'),
    InlineKeyboardButton(text='Месяц', callback_data='30')],
    [InlineKeyboardButton(text='❌а можно НЕ надо', callback_data='stop_write')]
    ])

back = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='❌а можно НЕ надо', callback_data='stop_write')]
    ])