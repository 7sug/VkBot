
import users
from users import User
import database
import monsters


class Bot:

    def __init__(self, user_id):
        print("Создан объект бота!")
        self.USER_ID = user_id
        self.COMMANDS = ["ПРИВЕТ", "РЕГИСТРАЦИЯ", "ПРОФИЛЬ", "ЛОКАЦИИ", "СТРАШНЫЕ ТВАРИ",
                         "ТЕМНЫЙ МАГАЗИН", "ИНВЕНТАРЬ", "ВЕСЕЛЫЕ ЦВЕТОЧКИ", "РАДУЖНЫЙ МАГАЗИН"]
        self.LOCATIONS = ["ТЕМНЫЙ ЛЕС", "РАДУЖНАЯ ПОЛЯНА", "ГЛАВНОЕ МЕНЮ"]
        self.item_name = ''

    def new_message(self, message, user_id, user_name):

        if message.upper() == self.COMMANDS[0]:
            return "Привет!"
        elif message.upper() == self.COMMANDS[1]:
            if database.check_uniq_user(user_id) == 0:
                new_user = User()
                database.insert_user(users.User.user_id, new_user.money,
                                     user_name, new_user.health, new_user.user_clan, new_user.power,
                                     user_id, new_user.exp, new_user.lvl)
                return f"Ты успешно зарегестрирован! Твои начальные характеристики:\n Здоровье: {new_user.health}\n " \
                       f"Уровень: {new_user.lvl}\n Деньги: {new_user.money} \n " \
                       f"Клан: {new_user.user_clan} \n Урон: {new_user.power}"
            else:
                return f"Вы уже зарегестрированны!"
        elif message.upper() == self.COMMANDS[2]:
            profile_array = database.show_profile(user_id)
            if profile_array is not None:
                return f"Вот твои данные:\n 👤 Имя 👤: {profile_array[1]} \n 🌐 Клан 🌐: {profile_array[3]} \n " \
                       f"❤ Здоровье ❤: {profile_array[2]} \n 💢 Сила 💢:" \
                       f" {profile_array[4]} \n 💵 Деньги 💵: {profile_array[0]} \n 💯 Уровень 💯: {profile_array[5]}"
            else:
                return f"Сначала нужно зарегистрироваться!"
        elif message.upper() == self.COMMANDS[3]:
            return f"Куда пойдем?"
        elif message.upper() == self.LOCATIONS[0]:
            return f"Ты в темном лесу"
        elif message.upper() == self.LOCATIONS[1]:
            return f"Ты на радужной поляне"
        elif message.upper() == self.LOCATIONS[2]:
            return f"Ты в главном меню"
        elif message.upper() == self.COMMANDS[4]:
            bd_name = 'dark_forest_monsters'
            return monsters.fight(user_id, bd_name)
        elif message.upper() == self.COMMANDS[7]:
            bd_name = 'rainbow_glade_monsters'
            return monsters.fight(user_id, bd_name)
        elif message.upper() == self.COMMANDS[5]:
            bd_name = 'dark_forest_shop'
            items_array = database.shop_show_items(bd_name)
            return f"Вот список предметов: {', '.join(items_array)}"
        elif message.upper() == self.COMMANDS[8]:
            bd_name = 'rainbow_glade_shop'
            items_array = database.shop_show_items(bd_name)
            return f"Вот список предметов: {', '.join(items_array)}"
        elif message.lower() == 'шапка' or message.lower() == 'палка' or message.lower() == 'железный меч' or \
                message.lower() == 'щит' or message.lower() == 'зачарованный клык' or \
                message.lower() == 'секира ужаса':
            bd_name = 'dark_forest_shop'
            return database.buy_items(user_id, message.lower(), bd_name)
        elif message.lower() == 'амулет силы' or message.lower() == 'амулет защиты' or\
                message.lower() == 'клинок пламени' or message.lower() == 'броня эльфов' or \
                message.lower() == 'кольцо бога':
            bd_name = 'RAINBOW_GLADE_SHOP'
            return database.buy_items(user_id, message.lower(), bd_name)
        elif message.upper() == self.COMMANDS[6]:
            inv = database.show_inventory(user_id)
            return f"Вот твой инвентарь: {', '.join(inv)}"
        elif message.lower() == 'таинственное подземелье':
            return f"Ты в таинственном подземелье..."

        else:
            return f"Я не знаю такой команды"


