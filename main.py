import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from VkBot import Bot

token = ''

api = vk_api.VkApi(token=token)
longpoll = VkLongPoll(api)


def message_vk(id, text):
    api.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print('New message:')
            print(f'For me by: {event.user_id}', end='')
            bot = Bot(event.user_id)
            message_vk(event.user_id, bot.new_message(event.text, event.user_id))
            print('Text: ', event.text)
