from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Form
from .users import user_storage
from .utils import get_current_temperature

router_profile = Router()

# Обработчик команды /start
@router_profile.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать! Я ваш бот.\nВведите /help для списка команд.")

@router_profile.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "Доступные команды:\n\n"
        " **Настройка профиля:**\n"
        "- /set_profile — Настроить ваш профиль (вес, рост, возраст, активность, город).\n\n"
        " **Логирование воды:**\n"
        "- /log_water <количество> — Записать количество выпитой воды (в мл).\n\n"
        " **Логирование еды:**\n"
        "- /log_food <название еды> — Записать съеденный продукт и его количество (в граммах).\n\n"
        " **Логирование тренировок:**\n"
        "- /log_workout <тип тренировки> <время (мин)> — Записать тренировку и рассчитать сожженные калории.\n"
        "  Поддерживаемые типы тренировок: бег, ходьба, велосипед, плавание, йога, силовая.\n\n"
        " **Добавление тренировки:**\n"
        "- /add_workout <название тренировки> <расход калорий в минуту> — Добавить новый тип тренировки.\n\n"
        " **Проверка прогресса:**\n"
        "- /check_progress — Показать текущий прогресс по воде и калориям.\n"
        "- /end_day — Подвести итоги за день.\n"
        "- /show_water_graph — Показать график потребления воды за последние 7 дней.\n"
        "- /show_calories_graph — Показать график потребления калорий за последние 7 дней.\n\n"
        " **Помощь:**\n"
        "- /help — Показать список команд."
    )
    await message.answer(help_text, parse_mode="MarkdownV2")


# Команда /set_profile
@router_profile.message(Command("set_profile"))
async def start_form(message: Message, state: FSMContext):
    await message.answer("Как Вас зовут?")
    await state.set_state(Form.name)

@router_profile.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    try:
        name = message.text
        await state.update_data(name=name)
        await message.answer(f"Приятно познакомиться, {name}! Введите ваш вес (в кг):")
        await state.set_state(Form.weight)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес.")

# Обработка веса
@router_profile.message(Form.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
        await state.update_data(weight=weight)
        await message.answer("Введите ваш рост (в см):")
        await state.set_state(Form.height)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес.")

# Обработка роста
@router_profile.message(Form.height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = float(message.text)
        await state.update_data(height=height)
        await message.answer("Введите ваш возраст:")
        await state.set_state(Form.age)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный рост.")

# Обработка возраста
@router_profile.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer("Сколько минут активности у вас в день?")
        await state.set_state(Form.activity)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст.")

# Обработка активности
@router_profile.message(Form.activity)
async def process_activity(message: Message, state: FSMContext):
    try:
        activity = int(message.text)
        await state.update_data(activity=activity)
        await message.answer("В каком городе вы находитесь?")
        await state.set_state(Form.city)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное количество минут активности.")

# Обработка города и завершение настройки профиля
@router_profile.message(Form.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text
    user_id = message.from_user.id

    # Получаем все данные из состояния
    user_data = await state.get_data()
    weight = user_data['weight']
    height = user_data['height']
    age = user_data['age']
    activity = user_data['activity']

    # Рассчет нормы воды и калорий
    current_temperature = await get_current_temperature(city)
    if current_temperature > 25:
        additional_water = 1000
    else:
        additional_water = 0

    water_goal = weight * 30 + (activity // 30) * 500 + additional_water
    calorie_goal = 10 * weight + 6.25 * height - 5 * age + (activity // 30) * 200

    # Сохраняем данные пользователя
    user_storage.set_user(user_id, {
        "weight": weight,
        "height": height,
        "age": age,
        "activity": activity,
        "city": city,
        "water_goal": water_goal,
        "calorie_goal": calorie_goal,
        "logged_water": 0,
        "logged_calories": 0,
        "burned_calories": 0
    })

    await state.clear()  # Завершаем состояние
    await message.answer(f"Профиль успешно настроен!\n\n"
                        f"Ваша дневная норма воды: {water_goal} мл\n"
                        f"Ваша дневная норма калорий: {calorie_goal} ккал")