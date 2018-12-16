import random
from threading import Thread

from vk_api import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from vk_bot.commands import auth, execute


def send(text, req, vk):
    print(text)
    vk.messages.send(random_id=random.randint(0, 10000000), peer_id=req.object.from_id,
                     message=text)


def exec(event, vk_api):
    text = execute(event)
    if text is not None and text != '':
        send(text, event, vk_api)


if __name__ == '__main__':


    vk = vk_api.VkApi(token=key)
    long_poll = VkBotLongPoll(vk, id)
    vk_api = vk.get_api()
    qb = auth()

    for event in long_poll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            thread = Thread(target=exec, args=(event, vk_api))
            thread.start()
