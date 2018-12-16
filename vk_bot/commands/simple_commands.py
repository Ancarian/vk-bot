import random

from vk_bot.commands.vk_methods import send


def reverse(req, vk):
    send(req.object.text[::-1], req, vk)


def upper(req, vk):
    send(req.object.text.upper(), req, vk)


def lower(req, vk):
    send(req.object.text.lower(), req, vk)


def shuffle(req, vk):
    text = req.object.text
    send(''.join(random.sample(text, len(text))), req, vk)


def is_running(req, vk):
    send('True', req, vk)
