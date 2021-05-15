import main

class Bot:
    checking_options = {'offset': 0, 'limit': 0, 'timeout': 0}

    def start(self):
        while True:
            try:
                self.update()
                main.sleep(1)
            except KeyboardInterrupt:
                print('Interrupted by the user')
                break

    def update(self):
        request = self.check_updates()
        if request:
            self.make_response(request)

    def check_updates(self):
        try:
            request = main.req.post(main.config.API_LINK + '/getUpdates', data=self.checking_options).json()
            # assert request.status_code == 200
        except:
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
                request = main.req.post(main.config.API_LINK + '/sendMessage', data=message_data)
            except:
                print('Send message error')
                return False

            if not request.status_code == 200:  # проверим статус пришедшего ответа
                return False

