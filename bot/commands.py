import os
import random

import psutil
import requests
from qbittorrent import Client


def auth():
    qb = Client('http://127.0.0.1:8080/')
    qb.login('admin', 'adminadmin')
    return qb


def shuffle(req):
    text = req['text']
    return ''.join(random.sample(text, len(text)))


def allowed_commands(req):
    return "allowed commands: {0}".format(str(', '.join([*commands])))


def test_connection(req):
    return 'bitTorrent: {0} \ncpu usage: {1}% \nmemory usage: {2}% \ndisc usage: {3}%'.format(
        requests.get('http://127.0.0.1:8080/').status_code, psutil.cpu_percent(), psutil.virtual_memory()[2],
        psutil.disk_usage('.')[3])


def parse_id(l, value):
    try:
        value = int(value) - 1
        if not len(l) > value >= 0:
            return None
        return value
    except ValueError:
        return None


def download(req):
    if len(req['attachments']) == 0:
        return 'no attachments'
    for attachment in req['attachments']:
        if attachment['type'] == 'doc' and attachment['ext'] == 'torrent':
            response = requests.get(attachment['link'], stream=True)
            with open(attachment['title'], "wb") as handle:
                handle.write(response.content)
            with open(attachment['title'], "rb") as handle:
                qb.download_from_file(handle)
    return 'download start'

def download_by_magnet_link(req):
    qb.download_from_link(req['text'])
    return 'download start'


def downloads(req):
    if len(qb.torrents()) == 0:
        return 'empty torrent list'
    return '\n'.join(
        ['{0}. {1} ({2})'.format(c, value['name'], value['state']) for c, value in enumerate(qb.torrents(), 1)])


def pause(req):
    value = parse_id(qb.torrents(), req['text'])
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
    value = parse_id(qb.torrents(), req['text'])
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
    value = parse_id(qb.torrents(), req['text'])
    if value is None:
        return 'incorrect value'
    torrent = qb.torrents()[value]
    qb.resume(torrent['hash'])
    return torrent['name'] + ' resumed'


def execute(req):
    if 'command' not in req or req['command'] not in commands:
        return "unknown command, allowed commands: {0}".format(str(', '.join([*commands])))

    return commands[req['command']](req)


commands = {
    'shuffle': shuffle,
    'commands': allowed_commands,
    'stats': test_connection,
    'download': download,
    'download-magnet': download_by_magnet_link,
    'torrents': downloads,
    'pause': pause,
    'pauseall': pause_all,
    'resume': resume,
    'resumeall': resume_all,
    'pausedownloaded': pause_all_downloaded_torrents,
    'delete': delete
}
qb = auth()
