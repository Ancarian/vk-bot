from vk_api import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from vk_bot.commands.commands import execute

if __name__ == '__main__':
    key = 'API TOKEN'
    id = 'GROUP ID'
    vk = vk_api.VkApi(token=key)
    long_poll = VkBotLongPoll(vk, id)
    vk_api = vk.get_api()

    for event in long_poll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            execute(event, vk_api)
