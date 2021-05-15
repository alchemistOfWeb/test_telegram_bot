import requests as req
import asyncio

from pprint import pprint
import config

from time import sleep


checking_options = {'offset': 0, 'limit': 0, 'timeout': 0}


def check_updates(data):
    try:
        request = req.post(config.API_LINK + '/getUpdates', data=data).json()
        # assert request.status_code == 200
    except:
        print('Error getting updates')
        return False

    if not request['ok']:
        return False

    return request


def make_response(request):
    for update in request['result']:
        global checking_options
        checking_options['offset'] = update['update_id'] + 1

        message = 'hello'
        if 'message' not in update or 'text' not in update['message']:
            message = "I can't understand it"


        message_data = {
            'chat_id': update['message']['chat']['id'],
            'text': message,
            'reply_to_message_id': update['message']['message_id'],
            'parse_mode': 'HTML'
        }

        try:
            request = req.post(config.API_LINK + '/sendMessage', data=message_data)
        except:
            print('Send message error')
            return False

        if not request.status_code == 200:  # проверим статус пришедшего ответа
            return False


if __name__ == '__main__':

    while True:
        try:
            request = check_updates(checking_options)
            if request:
                make_response(request)

            sleep(1)
        except KeyboardInterrupt:
            print('Interrupted by the user')
            break
