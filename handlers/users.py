class Users:
    def __init__(self):
        self.users = {}

    def get_user(self, user_id):
        return self.users.get(user_id)

    def set_user(self, user_id, data):
        self.users[user_id] = data
        
    def update_user(self, user_id, key, value):
        if user_id in self.users:
            self.users[user_id][key] = value

    def save_daily_progress(self, user_id):
        if user_id in self.users:
            user_data = self.users[user_id]
            if 'weekly_progress' not in user_data:
                user_data['weekly_progress'] = []

            # Инициализируем day_counter, если его нет
            if 'day_counter' not in user_data:
                user_data['day_counter'] = 0

            # Сохраняем текущий прогресс
            daily_progress = {
                'day': user_data['day_counter'],  # Используем day_counter вместо даты
                'logged_water': user_data.get('logged_water', 0),
                'logged_calories': user_data.get('logged_calories', 0),
                'burned_calories': user_data.get('burned_calories', 0)
            }

            # Добавляем в историю
            user_data['weekly_progress'].append(daily_progress)

            # Оставляем только последние 7 дней
            if len(user_data['weekly_progress']) > 7:
                user_data['weekly_progress'] = user_data['weekly_progress'][-7:]

            # Сбрасываем дневные значения
            user_data['logged_water'] = 0
            user_data['logged_calories'] = 0
            user_data['burned_calories'] = 0

            # Увеличиваем счетчик дней
            user_data['day_counter'] += 1

# Создаем экземпляр хранилища
user_storage = Users()