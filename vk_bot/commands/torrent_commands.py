import requests
from qbittorrent import Client

from vk_bot.commands.simple_commands import send


def auth():
    qb = Client('http://127.0.0.1:8080/')
    qb.login('admin', 'adminadmin')
    return qb


def get_value_in_range(l, value):
    try:
        value = int(value)
        if value is None or not len(l) > value >= 0:
            return None
        return value - 1
    except ValueError:
        return None

def download(req, vk):
    if len(req.object.attachments) == 0:
        send("no attachments", req, vk)
    else:
        for attachment in req.object.attachments:
            if attachment['type'] == 'doc' and attachment['doc']['ext'] == 'torrent':
                response = requests.get(attachment['doc']['url'], stream=True)
                with open(attachment['doc']['title'], "wb") as handle:
                    handle.write(response.content)
                with open(attachment['doc']['title'], "rb") as handle:
                    qb.download_from_file(handle)
                send(attachment['doc']['title'] + ' start download', req, vk)


def downloads(req, vk):
    if len(qb.torrents()) == 0:
        send('empty torrent list', req, vk)
    text = '\n'.join(
        ['{0}. {1} ({2})'.format(c, value['name'], value['state']) for c, value in enumerate(qb.torrents(), 1)])
    send(text, req, vk)


def pause(req, vk):
    value = get_value_in_range(qb.torrents(), req.object.text)
    if value is None:
        send('incorrect value', req, vk)
    torrent = qb.torrents()[value]
    qb.pause(torrent['hash'])
    send(torrent['name'] + ' paused', req, vk)


def resume(req, vk):
    value = get_value_in_range(qb.torrents(), req.object.text)
    if value is None:
        send('incorrect value', req, vk)
    torrent = qb.torrents()[value]
    qb.resume(torrent['hash'])
    send(torrent['name'] + ' resumed', req, vk)


qb = auth()
