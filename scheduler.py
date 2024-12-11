import asyncio
from datetime import datetime
from bot_file import bot
import datetime
import time
import admin.requests_admin as rq_adm

async def send_daily_message():
    while True:
        now = datetime.datetime.now()
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
        await asyncio.sleep(30)

async def check_birthdays():
    while True:
        admins = await rq_adm.get_all_admin()
        users = await rq_adm.check_birthday()
        for admin in admins:
            try:
                for user in users:
                    if users != '':
                        await bot.send_message(int(admin.tg_id), f'Хей, {datetime.datetime.strptime(str(user.birthday), "%Y-%m-%d").strftime("%d.%m")} '
                                    f'будет день рождения у сотрудника: {user.name_and_lastname}\n'
                                    f'Создай группу дня рождения! Исключи сотрудника, с tg_id: {user.tg_id}\n(ведь у него др)\n'
                                    f'В сообщение укажи:\nХело гайз, '
                                    f'{user.name_and_lastname} скоро будет праздновать свой др({datetime.datetime.strptime(str(user.birthday), "%Y-%m-%d").strftime("%d.%m")})\n'
                                    f'Давайте подумаем, что можно подарить и как будем отмечать?))\n'
                                    f'ТУТ ПРИЛОЖИ ССЫЛКУ НА СОЗДАННУЮ ГРУППУ')
                        await asyncio.sleep(86400)
            except ValueError as er:
                print(er)
                break
        await asyncio.sleep(43201)