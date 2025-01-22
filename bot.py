import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web
from aiogram.types import BotCommand
import os
from middlewares import LoggingMiddleware
from config import TOKEN
from handlers.profile import router_profile
from handlers.log import router_log
from handlers.statistics import router_st

bot = Bot(token=TOKEN)
dp = Dispatcher()

commands = [
    BotCommand(command="/start", description="Запустить бота"),
    BotCommand(command="/help", description="Показать список команд"),
    BotCommand(command="/set_profile", description="Настроить профиль"),
    BotCommand(command="/log_water", description="Записать количество воды"),
    BotCommand(command="/log_food", description="Записать съеденный продукт"),
    BotCommand(command="/log_workout", description="Записать тренировку"),
    BotCommand(command="/add_workout", description="Добавить тип тренировки"),
    BotCommand(command="/check_progress", description="Показать текущий прогресс"),
    BotCommand(command="/end_day", description="Подвести итоги за день"),
    BotCommand(command="/show_water_graph", description="График потребления воды"),
    BotCommand(command="/show_calories_graph", description="График потребления калорий"),
]

async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(commands)

dp.include_router(router_profile)
dp.include_router(router_log)
dp.include_router(router_st)
dp.update.middleware(LoggingMiddleware())
# async def main():
#     print("Бот запущен!")
#     await set_bot_commands(bot)
#     await dp.start_polling(bot)

async def handle(request):
    return web.Response(text="Бот запущен")

app = web.Application()
app.add_routes([web.get('/', handle)])

async def start_bot():
    await dp.start_polling(bot)

async def start_app():
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))  # Используем порт из переменной окружения
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    await asyncio.gather(start_bot(), start_app())

if __name__ == "__main__":
    asyncio.run(main())