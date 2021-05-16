from time import sleep
import requests as req


class Bot:

    __checking_options = {'offset': 0, 'limit': 0, 'timeout': 0}
    "contains settings of request for checking updates"

    __sleeping_time = 1
    "need to avoid too frequent requests to the telegram server"

    def __init__(self, bot_token, sleeping_time=1):
        self.api_link = f'https://api.telegram.org/bot{bot_token}'
        self.__sleeping_time = sleeping_time

    def run(self):
        while True:
            try:
                self.update()
                sleep(self.__sleeping_time)

            except KeyboardInterrupt:
                print('Interrupted by yourself')
                break

    def update(self):
        request = self.check_updates()

        if request:
            self.make_response(request)

    def check_updates(self):
        try:
            request = req.post(self.api_link + '/getUpdates', data=self.__checking_options).json()

        except Exception:
            print('error getting updates')
            return False

        if not request['ok'] or not request['result']:
            return False

        return request

    def make_response(self, request):
        for update in request['result']:
            self.__checking_options['offset'] = update['update_id'] + 1

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
            except Exception:
                print('Send message error')
                return False

            username = update['message']['chat']['first_name']
            print(f"sending message to {username}")
