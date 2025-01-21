import aiohttp
from config import USDA_KEY
from config import OPEN_W_KEY

async def get_food_info(product_name: str):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={USDA_KEY}&query={product_name}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    foods = data.get('foods', [])
                    if foods:
                        first_food = foods[0]
                        nutrients = first_food.get('foodNutrients', [])
                        for nutrient in nutrients:
                            if nutrient.get('nutrientName') == 'Energy':
                                return nutrient.get('value', 0)
    except aiohttp.ClientError:
        pass

    return 0

async def get_current_temperature(city: str) -> float:

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_W_KEY}&units=metric"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Температура находится в main.temp
                    temperature = data.get('main', {}).get('temp')
                    return temperature
                else:
                    return 0
    except aiohttp.ClientError as e:
        return None