import random

import requests


def reverse(req, vk):
    send(req.object.text[::-1], req, vk)


def upper(req, vk):
    send(req.object.text.upper(), req, vk)


def lower(req, vk):
    send(req.object.text.lower(), req, vk)


def comeback_to_2007(req, vk):
    text = req.object.text.lower()
    strr = ''
    for i in range(len(text)):
        if i % 2 != 0:
            strr += text[i].upper()
        else:
            strr += text[i]
    send(strr, req, vk)


def shuffle(req, vk):
    text = req.object.text
    send(''.join(random.sample(text, len(text))), req, vk)


def is_running(req, vk):
    send('True', req, vk)


def send(text, req, vk):
    print(text)
    if len(text) != 0:
        vk.messages.send(random_id=random.randint(0, 10000000), peer_id=req.object.from_id,
                         message=text)


def download(req, vk):
    print("download")
    if len(req.object.attachments) == 0:
        send("no attachments", req, vk)
    else:
        for attachment in req.object.attachments:
            if attachment['type'] == 'doc':
                response = requests.get(attachment['doc']['url'], stream=True)
                with open(attachment['doc']['title'], "wb") as handle:
                    handle.write(response.content)
                send(attachment['doc']['title'] + ' downloaded', req, vk)


def execute(req, vk):
    c = req.object.text.split(' ')
    print(c)
    if len(c) == 0 or c[0] not in commands:
        send("unknown command, exists commands: {0}".format(str(', '.join([*commands]))), req,
             vk)
        return
    elif len(c) > 1:
        req.object.text = ' '.join(c[1:])
    commands[c[0]](req, vk)


commands = {
    'reverse': reverse,
    'upper': upper,
    'lower': lower,
    '2007': comeback_to_2007,
    'shuffle': shuffle,
    'download': download,
    'test': is_running
}
