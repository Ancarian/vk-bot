import random

from vk_api import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from vk_bot.commands import execute


class Server:

    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                execute(event, self.vk_api)


if __name__ == '__main__':
    key = 'a7b69f837db6b8afdc1eb38ee4834739d4d97c442ec34f25fcbe00330d8b40a29e5f4a9ff0810e19d6fee'
    id = '175304786'
    Server(key, id).start()
