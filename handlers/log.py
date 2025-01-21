from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Food
from .users import user_storage
from .workout import workout_storage
from .utils import get_food_info
import random

router_log = Router()

@router_log.message(Command("log_water"))
async def log_water(message: Message):
    user_id = message.from_user.id

    # Получаем данные пользователя
    user_data = user_storage.get_user(user_id)
    if not user_data:
        await message.answer("Сначала настройте профиль с помощью /set_profile")
        return

    try:
        amount = int(message.text.split()[1])

        user_storage.update_user(user_id, 'logged_water', user_data['logged_water'] + amount)

        remaining = user_data['water_goal'] - user_data['logged_water']

        await message.answer(f"Записано: {amount} мл воды. Осталось выпить: {remaining} мл")
    except (IndexError, ValueError):
        await message.answer("Используйте команду так: /log_water <количество>")


food_info = {}
@router_log.message(Command("log_food"))
async def start_form(message: Message, state: FSMContext):
    user_id = message.from_user.id

    user_data = user_storage.get_user(user_id)
    if not user_data:
        await message.answer("Сначала настройте профиль с помощью /set_profile")
        return

    try:
        food = message.text.split()[1]
        calories_per_100 = await get_food_info(food)
        food_info['calories_per_100'] = calories_per_100
        await message.answer(f"Отличный вкус! Вы съели {food}. Калорийность {calories_per_100} ккал на 100 г. Сколько грамм вы съели?")
        await state.set_state(Food.grams)
    except (IndexError, ValueError):
        await message.answer("Используйте команду так: /log_food <название еды>")

low_calories_food = ('cucumber', 
                     'red wine', 
                     'cabbage', 
                     'apple', 
                     'Greek yogurt', 
                     'carrot', 
                     'broccoly', 
                     'spinach'
                     )

@router_log.message(Food.grams)
async def process_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = user_storage.get_user(user_id)
    if not user_data:
        await message.answer("Сначала настройте профиль с помощью /set_profile")
        return
    try:
        grams = int(message.text)
        amount = food_info['calories_per_100']/100*grams
        user_storage.update_user(user_id, 'logged_calories', user_data['logged_calories'] + amount)
        remaining = user_data['calorie_goal'] - user_data['logged_calories']
        await message.answer(f"Записано: {amount} ккал. Осталось {remaining} ккал.")
        await state.clear()
        if remaining <= 0:
            recomended_food = random.sample(low_calories_food, k=3)
            await message.answer(f'**Ой ой ой, кажется вы превысили свою дневную норму калорий.** \n\n' 
                                 f'Вот несколько низкокалорийных продуктов, которыми вы можете перекусить:\n'
                                 f'{recomended_food[0]} - {await get_food_info(recomended_food[0])} ккал на 100 г.\n'
                                 f'{recomended_food[1]} - {await get_food_info(recomended_food[1])} ккал на 100 г.\n'
                                 f'{recomended_food[2]} - {await get_food_info(recomended_food[2])} ккал на 100 г.\n')
        elif remaining < user_data['calorie_goal']*0.1:
            await message.answer(f'**Ой, кажется вы скоро достигните своей нормы калорий.**' 
                                 f'Вот несколько низкокалорийных продуктов, которыми вы можете перекусить:\n'
                                 f'{recomended_food[0]} - {await get_food_info(recomended_food[0])} ккал на 100 г.\n'
                                 f'{recomended_food[1]} - {await get_food_info(recomended_food[1])} ккал на 100 г.\n'
                                 f'{recomended_food[2]} - {await get_food_info(recomended_food[2])} ккал на 100 г.\n')

    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес.")


@router_log.message(Command("log_workout"))
async def log_workout(message: Message):
    user_id = message.from_user.id

    # Получаем данные пользователя
    user_data = user_storage.get_user(user_id)
    if not user_data:
        await message.answer("Сначала настройте профиль с помощью /set_profile")
        return

    try:
        # Парсим команду
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            raise ValueError

        workout_type = parts[1].lower()  # Тип тренировки
        duration = int(parts[2])        # Продолжительность в минутах

        # Получаем расход калорий для типа тренировки
        calories_per_min = workout_storage.get_workout(workout_type)
        if not calories_per_min:
            await message.answer(f"Тип тренировки '{workout_type}' не поддерживается.")
            return

        # Рассчитываем сожженные калории
        burned_calories = calories_per_min * duration

        # Рассчитываем дополнительное количество воды
        additional_water = (duration // 30) * 200
        
        # Обновляем данные пользователя
        user_storage.update_user(user_id, 'burned_calories', user_data['burned_calories'] + burned_calories)
        user_storage.update_user(user_id, 'logged_water', user_data['logged_water'] + additional_water)

        # Отправляем сообщение пользователю
        await message.answer(
            f"🏋️‍♂️ {workout_type.capitalize()} {duration} минут — {burned_calories} ккал.\n")
        if additional_water>0:
            await message.answer(
            f"Дополнительно: выпейте {additional_water} мл воды.")

    except (IndexError, ValueError):
        await message.answer("Используйте команду так: /log_workout <тип тренировки> <время (мин)>")

@router_log.message(Command("add_workout"))
async def add_workout(message: Message, state: FSMContext):
    user_id = message.from_user.id

    user_data = user_storage.get_user(user_id)
    if not user_data:
        await message.answer("Сначала настройте профиль с помощью /set_profile")
        return

    try:
        workout_type = message.text.split()[1]
        data = message.text.split()[2]
        workout_storage.set_workout(workout_type, data)
        await message.answer(f"Добавлена тренировка {workout_type}. Расход калорий в минуту: {data}")
    except (IndexError, ValueError):
        await message.answer("Используйте команду так: /add_workout <название тренировки> <расход калорий в минуту>")

