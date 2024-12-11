import asyncio
from aiogram import Dispatcher

from database.models import async_main
from handlers.handlers import router
from admin.handlers_admin import router_adm
from bot_file import bot
from send_messages import reminders

dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(router)
    dp.include_router(router_adm)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
        asyncio.run(reminders())
    except KeyboardInterrupt:
        print('Goodbay!')