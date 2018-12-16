import random

import psutil
import requests
from qbittorrent import Client


def auth():
    qb = Client('http://127.0.0.1:8080/')
    qb.login('admin', 'adminadmin')
    return qb


def shuffle(req):
    text = req.object.text
    return ''.join(random.sample(text, len(text)))


def allowed_commands(req):
    return "allowed commands: {0}".format(str(', '.join([*commands])))


def test_connection(req):
    return 'bitTorrent: {0} \ncpu usage: {1}% \nmemory usage: {2}% \ndisc usage: {3}%'.format(
        requests.get('http://127.0.0.1:8080/').status_code, psutil.cpu_percent(), psutil.virtual_memory()[2],
        psutil.disk_usage('.')[3])


def get_value_if_in_range(l, value):
    try:
        value = int(value) - 1
        if not len(l) > value >= 0:
            return None
        return value
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
    return 'download start'


def downloads(req):
    if len(qb.torrents()) == 0:
        return 'empty torrent list'
    return '\n'.join(
        ['{0}. {1} ({2})'.format(c, value['name'], value['state']) for c, value in enumerate(qb.torrents(), 1)])


def pause(req):
    value = get_value_if_in_range(qb.torrents(), req.object.text)
    if value is None:
        return 'incorrect value'
    torrent = qb.torrents()[value]
    qb.pause(torrent['hash'])
    return torrent['name'] + ' paused'


def pause_all(req):
    qb.pause_all()
    return 'pause all'


def resume_all(req):
    qb.resume_all()
    return 'resume all'


def delete(req):
    value = get_value_if_in_range(qb.torrents(), req.object.text)
    if value is None:
        return 'incorrect value'
    torrent = qb.torrents()[value]
    qb.delete_permanently(torrent['hash'])
    return torrent['name'] + ' deleted'


def pause_all_downloaded_torrents(req):
    torrents = qb.torrents(filter='completed')
    hashes = [torrent['hash'] for torrent in torrents]
    qb.pause_multiple(hashes)
    return 'pause all downloaded torrents'


def resume(req):
    value = get_value_if_in_range(qb.torrents(), req.object.text)
    if value is None:
        return 'incorrect value'
    torrent = qb.torrents()[value]
    qb.resume(torrent['hash'])
    return torrent['name'] + ' resumed'


def execute(req):
    c = req.object.text.split(' ', 1)
    if len(c) == 0 or c[0] not in commands:
        return "unknown command, allowed commands: {0}".format(str(', '.join([*commands])))
    elif len(c) > 1:
        req.object.text = c[1]
    return commands[c[0]](req)


commands = {
    'shuffle': shuffle,
    'commands': allowed_commands,
    'stats': test_connection,
    'download': download,
    'torrents': downloads,
    'pause': pause,
    'pauseall': pause_all,
    'resume': resume,
    'resumeall': resume_all,
    'pausedownloaded': pause_all_downloaded_torrents,
    'delete': delete
}
qb = auth()
