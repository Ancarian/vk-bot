import random

from vk_api import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from vk_bot.commands.commands import execute


def send(text, req, vk):
    print(text)
    if len(text) != 0:
        vk.messages.send(random_id=random.randint(0, 10000000), peer_id=req.object.from_id,
                         message=text)


if __name__ == '__main__':
    key = 'API TOKEN'
    id = 'GROUP ID'
    vk = vk_api.VkApi(token=key)
    long_poll = VkBotLongPoll(vk, id)
    vk_api = vk.get_api()

    for event in long_poll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = execute(event)
            send(text, event, vk_api)
