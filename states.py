from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    age = State()
    weight = State()
    height = State()
    activity = State()
    city = State()
    
class Food(StatesGroup):
    grams = State()