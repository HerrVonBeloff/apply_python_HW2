from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from .users import user_storage
import matplotlib.pyplot as plt
import io
from aiogram.types import BufferedInputFile

router_st = Router()

@router_st.message(Command("check_progress"))
async def check_progress(message: Message):
    user_id = message.from_user.id

    # Получаем данные пользователя
    user_data = user_storage.get_user(user_id)
    if not user_data:
        await message.answer("Сначала настройте профиль с помощью /set_profile")
        return

    # Получаем текущие значения
    logged_water = user_data.get('logged_water', 0)
    water_goal = user_data.get('water_goal', 0)
    remaining_water = water_goal - logged_water

    logged_calories = user_data.get('logged_calories', 0)
    burned_calories = user_data.get('burned_calories', 0)
    calorie_goal = user_data.get('calorie_goal', 0)
    remaining_calories = calorie_goal - logged_calories + burned_calories

    # Формируем сообщение с прогрессом
    progress_message = (
        "📊 Прогресс:\n\n"
        f"Вода:\n"
        f"- Выпито: {logged_water} мл из {water_goal} мл.\n"
        f"- Осталось: {remaining_water} мл.\n\n"
        f"Калории:\n"
        f"- Потреблено: {logged_calories} ккал из {calorie_goal} ккал.\n"
        f"- Сожжено: {burned_calories} ккал.\n"
        f"- Баланс: {remaining_calories} ккал."
    )

    await message.answer(progress_message)


@router_st.message(Command("end_day"))
async def end_day(message: Message):
    user_id = message.from_user.id
    user_data = user_storage.get_user(user_id)
    if not user_data:
        await message.answer("Сначала настройте профиль с помощью /set_profile")
        return

    # Получаем текущие значения перед сбросом
    total_water = user_data.get('logged_water', 0)
    total_calories = user_data.get('logged_calories', 0)
    total_burned = user_data.get('burned_calories', 0)

    # Сохраняем прогресс за день
    user_storage.save_daily_progress(user_id)

    # Выводим итоги за сегодня
    await message.answer(
        f"Итоги за день #{user_data['day_counter'] - 1}:\n"
        f"🌊 Выпито воды: {total_water} мл\n"
        f"🍽️ Потреблено калорий: {total_calories} ккал\n"
        f"🔥 Сожжено калорий: {total_burned} ккал\n\n"
        f"Используйте /show_water_graph или /show_calories_graph для построения графиков за последние 7 дней."
    )

@router_st.message(Command("show_water_graph"))
async def show_water_graph(message: Message):
    user_id = message.from_user.id
    user_data = user_storage.get_user(user_id)
    if not user_data: 
        await message.answer("Сначала настройте профиль с помощью /set_profile")
        return

    weekly_progress = user_data.get('weekly_progress', [])
    if not weekly_progress:
        await message.answer("Нет данных за последние 7 дней.")
        return

    # Получаем данные
    days = [day['day'] for day in weekly_progress]
    water = [day['logged_water'] for day in weekly_progress]

    # Создаем график с помощью matplotlib
    plt.figure(figsize=(10, 5))
    plt.plot(days, water, marker='o', linestyle='-', linewidth=2, markersize=8)
    plt.fill_between(days, water, alpha=0.2)
    plt.xticks(days)
    plt.legend(['Выпито воды (мл)'])
    plt.title("Потребление воды за последние 7 дней")
    plt.xlabel("День")
    plt.ylabel("Количество воды (мл)")
    plt.grid(True)

    # Сохраняем график в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Отправляем изображение
    await message.answer_photo(BufferedInputFile(buf.read(), filename="water_graph.png"))

@router_st.message(Command("show_calories_graph"))
async def show_calories_graph(message: Message):
    user_id = message.from_user.id
    user_data = user_storage.get_user(user_id)
    if not user_data:
        await message.answer("Сначала настройте профиль с помощью /set_profile")
        return

    weekly_progress = user_data.get('weekly_progress', [])
    if not weekly_progress:
        await message.answer("Нет данных за последние 7 дней.")
        return

    # Получаем данные
    days = [day['day'] for day in weekly_progress]
    calories = [day['logged_calories'] for day in weekly_progress]

    # Создаем график с помощью matplotlib
    plt.figure(figsize=(10, 5))
    plt.plot(days, calories, marker='o', color='darkorange', linestyle='-', linewidth=2, markersize=8)
    plt.fill_between(days, calories, color='darkorange', alpha=0.2)
    plt.xticks(days)
    plt.legend(['Потреблено калорий (ккал)'])
    plt.title("Потребление калорий за последние 7 дней")
    plt.xlabel("День")
    plt.ylabel("Количество калорий (ккал)")
    plt.grid(True)

    # Сохраняем график в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Отправляем изображение
    await message.answer_photo(BufferedInputFile(buf.read(), filename="calories_graph.png"))