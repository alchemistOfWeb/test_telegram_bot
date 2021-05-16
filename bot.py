from time import sleep
import requests as req


class Bot:
    checking_options = {'offset': 0, 'limit': 0, 'timeout': 0}

    def __init__(self, bot_token):
        self.api_link = f'https://api.telegram.org/bot{bot_token}'

    def run(self):
        while True:
            try:
                self.update()
                sleep(1)

            except KeyboardInterrupt:
                print('Interrupted by yourself')
                break

    def update(self):
        request = self.check_updates()

        if request:
            self.make_response(request)

    def check_updates(self):
        try:
            request = req.post(self.api_link + '/getUpdates', data=self.checking_options).json()
        except Exception:
            print('error getting updates')
            return False

        if not request['ok'] or not request['result']:
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
                request = req.post(self.api_link + '/sendMessage', data=message_data)
                username = update['message']['chat']['first_name']
                print(f"sending message to {username}")
            except Exception:
                print('Send message error')
                return False

            if not request.status_code == 200:
                return False
