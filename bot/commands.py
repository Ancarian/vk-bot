import random

import psutil
import requests

from bot.utils import get_connection, parse_id, create_incorrect_id_message


def shuffle(req):
    text = req['text']
    return ''.join(random.sample(text, len(text)))


def allowed_commands(req):
    return "allowed commands: {0}".format(str(', '.join([*commands])))


def test_connection(req):
    return 'cpu usage: {0}% \nmemory usage: {1}% \ndisc usage: {2}%'.format(
        psutil.cpu_percent(), psutil.virtual_memory()[2], psutil.disk_usage('.')[3])


def download(req):
    if len(req['attachments']) == 0:
        return 'no attachments'
    conn = get_connection()
    for attachment in req['attachments']:
        if attachment['type'] == 'doc' and attachment['ext'] == 'torrent':
            response = requests.get(attachment['link'], stream=True)
            filepath = '../torrents/' + attachment['title']
            with open(filepath, "wb") as handle:
                handle.write(response.content)
            with open(filepath, "rb") as handle:
                conn.download_from_file(handle)
    return 'download start'


def download_by_magnet_link(req):
    get_connection().download_from_link(req['text'])
    return 'download start'


def downloads(req):
    conn = get_connection()
    if len(conn.torrents()) == 0:
        return 'empty torrent list'
    return '\n'.join(
        ['{0}. {1} ({2})'.format(c, value['name'], value['state']) for c, value in
         enumerate(conn.torrents(), 1)])


def pause(req):
    conn = get_connection()
    value = parse_id(conn.torrents(), req['text'])
    if value is None:
        return create_incorrect_id_message(conn, req)
    torrent = conn.torrents()[value]
    conn.pause(torrent['hash'])
    return torrent['name'] + ' paused'


def pause_all(req):
    get_connection().pause_all()
    return 'pause all'


def resume_all(req):
    get_connection().resume_all()
    return 'resume all'


def delete(req):
    conn = get_connection()
    value = parse_id(conn.torrents(), req['text'])
    if value is None:
        return create_incorrect_id_message(conn, req)
    torrent = conn.torrents()[value]
    conn.delete_permanently(torrent['hash'])
    return torrent['name'] + ' deleted'


def pause_all_downloaded_torrents(req):
    conn = get_connection()
    torrents = conn.torrents(filter='completed')
    hashes = [torrent['hash'] for torrent in torrents]
    conn.pause_multiple(hashes)
    return 'pause all downloaded torrents'


def resume(req):
    conn = get_connection()
    value = parse_id(conn.torrents(), req['text'])
    if value is None:
        return create_incorrect_id_message(conn, req)
    torrent = conn.torrents()[value]
    conn.resume(torrent['hash'])
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
    'd': download,
    'download-magnet': download_by_magnet_link,
    'dm': download_by_magnet_link,
    'torrents': downloads,
    'pause': pause,
    'pauseall': pause_all,
    'pall': pause_all,
    'resume': resume,
    'resumeall': resume_all,
    'rall': resume_all,
    'pausedownloaded': pause_all_downloaded_torrents,
    'pausedd': pause_all_downloaded_torrents,
    'delete': delete
}
