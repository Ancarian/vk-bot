import requests
from qbittorrent import Client

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


def download(req):
    if len(req.object.attachments) == 0:
        return 'no attachments'
    for attachment in req.object.attachments:
        if attachment['type'] == 'doc' and attachment['doc']['ext'] == 'torrent':
            response = requests.get(attachment['doc']['url'], stream=True)
            with open(attachment['doc']['title'], "wb") as handle:
                handle.write(response.content)
            with open(attachment['doc']['title'], "rb") as handle:
                qb.download_from_file(handle)
            return attachment['doc']['title'] + ' start download'


def downloads(req):
    if len(qb.torrents()) == 0:
        return 'empty torrent list'
    return '\n'.join(
        ['{0}. {1} ({2})'.format(c, value['name'], value['state']) for c, value in enumerate(qb.torrents(), 1)])


def delete(req):
    value = get_value_in_range(qb.torrents(), req.object.text)
    if value is None:
        return 'incorrect value'
    torrent = qb.torrents()[value]
    qb.pause(torrent['hash'])
    return torrent['name'] + ' paused'

def pause(req):
    value = get_value_in_range(qb.torrents(), req.object.text)
    if value is None:
        return 'incorrect value'
    torrent = qb.torrents()[value]
    qb.pause(torrent['hash'])
    return torrent['name'] + ' paused'


def resume(req):
    value = get_value_in_range(qb.torrents(), req.object.text)
    if value is None:
        return 'incorrect value'
    torrent = qb.torrents()[value]
    qb.resume(torrent['hash'])
    return torrent['name'] + ' resumed'


qb = auth()
