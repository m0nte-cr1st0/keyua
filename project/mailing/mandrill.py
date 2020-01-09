# Python imports
import requests

# Django imports
from django.conf import settings


def mandrill_sent_letter(body, uri=False):
    if not uri:
        uri = 'messages/send.json'
    url = '%s%s' % (settings.MANDRILL_API_URL, uri)

    print(body)

    resp = requests.post(url=url, data=body)

    answer = clean_mandrill_answer(resp.text)
    print(answer)

    if answer['status'] == 'error':
        if 'message' in answer:
            raise Exception('%s' % answer['message'])
        else:
            print(u'Unknown error: %s' % answer)
    else:
        return answer['_id']


def clean_mandrill_answer(answer):
    answer = answer.replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('"', '')
    dict_answer = {}
    for pair in answer.split(','):
        if pair.split(':')[0] in ['email', '_id', 'status', 'message']:
            dict_answer[pair.split(':')[0]] = pair.split(':')[1]
    return dict_answer