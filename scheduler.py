import asyncio
from datetime import datetime
from bot_file import bot

async def send_daily_message():
    while True:
        now = datetime.now()
        if now.weekday() == 0 and now.hour == 11 and now.minute == 5:
            await bot.send_message(-1004565238773, "Гайз, напоминаю еще раз об оплате обедов, тем кто ел за прошлые разы))")
        if now.weekday() == 4 and now.hour == 18 and now.minute == 0:
            await bot.send_message(-1004565238773, "Реби, наконец-то пятница!\nЭто напоминалка о том, что можно занести кэш, тем кто обедал всю эту неделю❤️‍🩹")
        if now.day == 13 and now.hour == 12 and now.minute == 0:
            await bot.send_message(-1001887207578, "Реби, я бот-ассистент нашего офис-менеджера😎\nНапоминаю, что через меня вы можете заказать всяких ништяков в студию))\n"
                                                   "Всем пис, айл би бэк✨")
        if now.day == 28 and now.hour == 12 and now.minute == 0:
            await bot.send_message(-1001887207578, "Реби, я бот-ассистент нашего офис-менеджера😎\nНапоминаю, что через меня вы можете заказать всяких ништяков в студию))\n"
                                                   "Всем пис, айл би бэк✨")
        await asyncio.sleep(60)