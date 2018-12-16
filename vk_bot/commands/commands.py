
from vk_bot.commands.simple_commands import reverse, upper, lower, shuffle, is_running
from vk_bot.commands.torrent_commands import downloads, pause, resume, download


def execute(req):
    c = req.object.text.split(' ')
    if len(c) == 0 or c[0] not in commands:
        return "unknown command, exists commands: {0}".format(str(', '.join([*commands])))
    elif len(c) > 1:
        req.object.text = ' '.join(c[1:])
    return commands[c[0]](req)


commands = {
    'reverse': reverse,
    'upper': upper,
    'lower': lower,
    'shuffle': shuffle,
    'download': download,
    'test': is_running,
    'downloads': downloads,
    'pause': pause,
    'resume': resume
}
