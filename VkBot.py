import users
from users import User
import database


class Bot:
    def __init__(self, user_id):
        print("Создан объект бота!")
        self.USER_ID = user_id
        self.COMMANDS = ["ПРИВЕТ", "РЕГИСТРАЦИЯ"]

    def new_message(self, message):
        if message.upper() == self.COMMANDS[0]:
            return "Привет!"
        elif message.upper() == self.COMMANDS[1]:
            new_user = User()
            user_name = 'User'
            database.insert_user(users.User.user_id, new_user.money, user_name, new_user.health)
            return f"Ты успешно зарегестрирован! Твои начальные характеристики:\n Здоровье: {new_user.health}\n " \
                   f"Опыт: {new_user.exp}\n Деньги: {new_user.money}"


