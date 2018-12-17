import random
from threading import Thread

from vk_api import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from commands import execute
from request_parser import parse_vk_request
from utils import parse_credentials, create_torrent_folder


def exec(event, vk_api):
    text = execute(parse_vk_request(event))
    if text is not None and text != '':
        vk_api.messages.send(random_id=random.randint(0, 10000000), peer_id=event.object.from_id,
                             message=text)


if __name__ == '__main__':
    credentials = parse_credentials()
    print(credentials)
    vk = vk_api.VkApi(token=credentials[0])
    long_poll = VkBotLongPoll(vk, credentials[1])
    vk_api = vk.get_api()
    create_torrent_folder()

    for event in long_poll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            thread = Thread(target=exec, args=(event, vk_api))
            thread.start()
