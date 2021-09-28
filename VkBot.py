import users
from users import User
import database


class Bot:
    def __init__(self, user_id):
        print("Создан объект бота!")
        self.USER_ID = user_id
        self.COMMANDS = ["ПРИВЕТ", "РЕГИСТРАЦИЯ", "ПРОФИЛЬ"]

    def new_message(self, message, user_id, user_name):
        if message.upper() == self.COMMANDS[0]:
            return "Привет!"
        elif message.upper() == self.COMMANDS[1]:
            print(database.check_uniq_user(user_id))
            if database.check_uniq_user(user_id) == 0:
                new_user = User()
                database.insert_user(users.User.user_id, new_user.money,
                                     user_name, new_user.health, new_user.user_clan, new_user.power, user_id)
                return f"Ты успешно зарегестрирован! Твои начальные характеристики:\n Здоровье: {new_user.health}\n " \
                       f"Опыт: {new_user.exp}\n Деньги: {new_user.money} \n " \
                       f"Клан: {new_user.user_clan} \n Урон: {new_user.power}"
            else:
                return f"Вы уже зарегестрированны!"
        elif message.upper() == self.COMMANDS[2]:
            profile_array = database.show_profile(user_id)
            return f"Вот твои данные:\n Имя: {profile_array[1]} \n Клан: {profile_array[3]} \n " \
                   f"Здоровье: {profile_array[2]} \n Сила: {profile_array[4]} \n Деньги: {profile_array[0]}"
        else:
            return f"Я не знаю такой команды"


