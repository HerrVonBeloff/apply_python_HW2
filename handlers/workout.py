class Workout:
    def __init__(self):
        self.workout = {}

    def get_workout(self, workout_type):
        return self.workout.get(workout_type)

    def set_workout(self, workout_type, data):
        self.workout[workout_type] = data

# Создаем экземпляр хранилища
workout_storage = Workout()

workout_storage.set_workout('бег', 10)
workout_storage.set_workout('ходьба', 5)
workout_storage.set_workout('велосипед', 8)
workout_storage.set_workout('йога', 3)
workout_storage.set_workout('силовая', 6)