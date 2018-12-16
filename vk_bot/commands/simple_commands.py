import random
import time


def reverse(req):
    return req.object.text[::-1]


def upper(req):
    return req.object.text.upper()


def lower(req):
    return req.object.text.lower()


def shuffle(req):
    text = req.object.text
    return ''.join(random.sample(text, len(text)))


def test_long_func(req):
    time.sleep(10)
    return 'executed'


def is_running(req):
    return 'True'
