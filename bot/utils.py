import os

from qbittorrent import Client
from vk_api import LoginRequired


def get_torrent_connection():
    qb = Client('http://127.0.0.1:8080/')
    try:
        # check connection. Throw exception if token expired
        qb.torrents()
    except LoginRequired:
        # get new token
        print("get new token")
        qb.login('admin', 'adminadmin')
    return qb


def parse_credentials():
    with open('credentials.txt', 'r') as f:
        return f.read().splitlines()


def parse_id(l, value):
    try:
        value = int(value) - 1
        if not len(l) > value >= 0:
            return None
        return value
    except ValueError:
        return None


def create_incorrect_id_message(conn, req):
    torrents_count = len(conn.torrents())
    if torrents_count == 0:
        return "empty torrent list"
    return 'incorrect [id] value, for example try {0} {1}'.format(req['command'], 1)


def create_torrent_folder():
    if not os.path.isdir('../torrents'):
        os.mkdir('../torrents')
