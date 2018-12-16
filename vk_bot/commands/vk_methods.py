import random


def send(text, req, vk):
    print(text)
    if len(text) != 0:
        vk.messages.send(random_id=random.randint(0, 10000000), peer_id=req.object.from_id,
                         message=text)
