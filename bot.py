import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
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

async def main():
    print("Бот запущен!")
    await set_bot_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())