from time import sleep
import requests as req


class Bot:
    checking_options = {'offset': 0, 'limit': 0, 'timeout': 0}

    def __init__(self, bot_token):
        self.API_LINK = f'https://api.telegram.org/bot{bot_token}'

    def run(self):
        while True:
            try:
                sleep(1)
                request = self.check_updates()

                if request:
                    self.make_response(request)

            except KeyboardInterrupt:
                print('Interrupted by yourself')
                break

    def update(self):
        pass

    def check_updates(self):
        try:
            request = req.post(self.API_LINK + '/getUpdates', data=self.checking_options).json()
        except Exception:
            print('Error getting updates')
            return False

        if not request['ok']:
            return False

        return request

    def make_response(self, request):
        for update in request['result']:
            self.checking_options['offset'] = update['update_id'] + 1

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
                request = req.post(self.API_LINK + '/sendMessage', data=message_data)
            except Exception:
                print('Send message error')
                return False

            if not request.status_code == 200:  # проверим статус пришедшего ответа
                return False

