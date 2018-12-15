import time

from vk_api import vk_api

from vk_bot.commands import execute, commands

command = 'kokoko'


def parse_credentials():
    with open('credentials.txt', 'r', encoding='utf-8') as f:
        return f.readlines()


def auth(login, password):
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    return vk_session.get_api()


def parse_new_messages(messages, vk):
    for message in messages:
        conversation = message['conversation']
        peer = conversation['peer']['id']
        out_read = conversation['out_read']
        count = conversation['unread_count']
        unread_messages = vk.messages.getHistory(start_message_id=out_read, count=count, peer_id=peer)
        for unread_message in unread_messages['items']:
            parse_command(unread_message, peer, vk)
        vk.messages.markAsRead(peer_id=peer, start_message_id=out_read)


def parse_command(text, peer, vk):
    text = text['text']
    text = text.lower()
    if command not in text:
        return
    c = text.split(' ')
    execute(c[1], ' '.join(c[2:]), peer, vk)


def run_listener():
    credentials = parse_credentials()
    vk = auth(credentials[0], credentials[1])

    while True:
        time.sleep(5)
        json = vk.messages.getConversations(filter='unread')
        if 'items' in json:
            parse_new_messages(json['items'], vk)


if __name__ == '__main__':
    print("unknown {0} command, exists commands: {1}".format("ggg", str(', '.join([*commands]))))
    print("start")
    run_listener()
