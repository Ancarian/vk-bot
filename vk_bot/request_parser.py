'''

PARSED REQ:
    {
    command: comm
    text: text
    attachments: {
        type: type
        link: link
        ext: ext
        title: titlee
        }
    }

'''


def parse_vk_request(request):
    parsed_req = {}

    c = request.object.text.split(' ', 1)
    if len(c) != 0:
        parsed_req['command'] = c[0]
        if len(c) > 1:
            parsed_req['text'] = c[1]
        else:
            parsed_req['text'] = ''
    if len(request.object.attachments) != 0:
        parsed_req['attachments'] = []
        for attachment in request.object.attachments:
            if 'doc' in attachment:
                attach = {'type': attachment['type'], 'ext': attachment['doc']['ext'], 'link': attachment['doc']['url'],
                          'title': attachment['doc']['title']}
                parsed_req['attachments'].append(attach)

    return parsed_req


def parse_telegram_request(request):
    pass
