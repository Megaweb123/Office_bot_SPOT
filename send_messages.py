from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from bot_file import bot

async def monday_dinner():
    bot.send_message('-1004565238773', "Гайз, напоминаю еще раз об оплате обедов, тем кто ел за прошлые разы))")

async def friday_dinner():
    bot.send_message('-1004565238773', "Реби, наконец-то пятница!\nЭто напоминалка о том, что можно занести кэш, тем кто обедал всю эту неделю❤️‍🩹")

async def bot_info():
    bot.send_message('-1001887207578', 'Реби, я бот-ассистент нашего офис-менеджера😎\nНапоминаю, что через меня вы можете заказать всяких ништяков в студию))\n'
                    'Всем пис, айл би бэк✨')

async def reminders():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(monday_dinner, 'cron', day_of_week='mon', hour=11, minute=5)
    scheduler.add_job(friday_dinner, 'cron', day_of_week='fri', hour=11, minute=5)
    scheduler.add_job(bot_info, 'cron', day=13, hour=12, minute=0)
    scheduler.add_job(bot_info, 'cron', day=28, hour=12, minute=0)

    scheduler.start()

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()