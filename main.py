import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from VkBot import Bot
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Регистрация', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Профиль', color=VkKeyboardColor.POSITIVE)


token = '366cc4368436cc5036e3928d2f387d147d2de7ef0f9eaa31d69ad9ef77bd3b1f5f32722bb7c2e55cd4f71'

api = vk_api.VkApi(token=token)
longpoll = VkLongPoll(api)


def message_vk(id, text):
    api.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard.get_keyboard()})


print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print('New message:')
            print(f'For me by: {event.user_id}', end='')
            bot = Bot(event.user_id)
            user_stats = api.method('users.get', {'user_ids': event.user_id})
            user_get = user_stats[0]
            user_name = user_get['first_name']
            message_vk(event.user_id, bot.new_message(event.text, event.user_id, user_name))
            print('Text: ', event.text)
