import random


def reverse(text, peer, vk):
    send(text[::-1], peer, vk)


def upper(text, peer, vk):
    send(text.upper(), peer, vk)


def lower(text, peer, vk):
    send(text.lower(), peer, vk)


def y2007(text, peer, vk):
    text = text.lower()
    strr = ''
    for i in range(len(text)):
        if i % 2 != 0:
            strr += text[i].upper()
        else:
            strr += text[i]
    send(strr, peer, vk)


def shuffle(text, peer, vk):
    send(''.join(random.sample(text, len(text))), peer, vk)


def send(text, peer, vk):
    vk.messages.send(random_id=random.randint(0, 10000000), peer_id=peer,
                     message=text)


def execute(command, text, peer, vk):
    print('command: {0}, text: {1}, peer: {2}'.format(command, text, peer))
    if command not in commands:
        send("unknown {0} command, exists commands: {1}".format(command, str(', '.join([*commands]))), peer, vk)
    commands[command](text, peer, vk)


commands = {
    'reverse': reverse,
    'upper': upper,
    'lower': lower,
    '2007': y2007,
    'shuffle': shuffle
}
