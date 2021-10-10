import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import re

import database
import monsters
from VkBot import Bot

import time


keyboard = open("keyboards/default.json", "r", encoding="UTF-8").read()

token = '366cc4368436cc5036e3928d2f387d147d2de7ef0f9eaa31d69ad9ef77bd3b1f5f32722bb7c2e55cd4f71'

api = vk_api.VkApi(token=token)
longpoll = VkLongPoll(api)


def change_keyboard(text):
    if text == 'Локации':
        keyboard = open("keyboards/locations.json", "r", encoding="UTF-8").read()
    elif text == 'Главное меню':
        keyboard = open("keyboards/default.json", "r", encoding="UTF-8").read()
    elif text == 'Темный лес':
        keyboard = open("keyboards/dark_forest.json", "r", encoding="UTF-8").read()
    elif text == 'Радужная поляна':
        keyboard = open("keyboards/rainbow_glade.json", "r", encoding="UTF-8").read()
    elif text == 'Темный магазин':
        keyboard = open("keyboards/dark_forest_items.json", "r", encoding="UTF-8").read()
    elif text == 'Радужный магазин':
        keyboard = open("keyboards/rainbow_glade_items.json", "r", encoding="UTF-8").read()
    elif text == 'Страшные твари':
        keyboard = open("keyboards/dark_forest.json", "r", encoding="UTF-8").read()
    elif text == 'Веселые цветочки':
        keyboard = open("keyboards/rainbow_glade.json", "r", encoding="UTF-8").read()
    elif text == 'Таинственное подземелье':
        keyboard = open("keyboards/mystery_dungeon.json", "r", encoding="UTF-8").read()
    else:
        keyboard = open("keyboards/default.json", "r", encoding="UTF-8").read()
    return keyboard


def message_vk(id, text):
    api.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard})


def test_message(id, fight_data):
    a = ''
    for i in fight_data:
        s = str(i)
        s1 = re.sub("[{|}|']", "", s)
        a += str(s1) + '\n'
    api.method('messages.send', {'user_id': id, 'message': a, 'random_id': 0, 'keyboard': keyboard})


print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            #print('New message:')
            #print(f'For me by: {event.user_id}', end='')
            bot = Bot(event.user_id)
            user_stats = api.method('users.get', {'user_ids': event.user_id})
            user_get = user_stats[0]
            user_name = user_get['first_name']
            keyboard = change_keyboard(event.text)
            if event.text == 'Страшные твари':
                test_message(event.user_id, monsters.fight(event.user_id, 'dark_forest_monsters'))
            elif event.text == 'Веселые цветочки':
                test_message(event.user_id, monsters.fight(event.user_id, 'rainbow_glade_monsters'))
            elif event.text == 'Поворот налево':
                test_message(event.user_id, monsters.boss_fight(event.user_id, 'bosses', 'Багровый демон', 'черный ключ'))
            elif event.text == 'Поворот направо':
                test_message(event.user_id, monsters.boss_fight(event.user_id, 'bosses', 'Дракон печали', 'зеленый ключ'))
            else:
                message_vk(event.user_id, bot.new_message(event.text, event.user_id, user_name))
                #print('Text: ', event.text)



