import requests

class Teleq:
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

    def get_updates(self, offset=None, timeout=5): # TIMEOUT
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result = resp.json()['result']
        return result

    def get_last_update(self):
        result = self.get_updates()

        if len(result) > 0:
            last_update = result[-1]
        else:
            last_update = None # NOTE Don't forget to handle None

        return last_update

    def send_message(self, chat_id, text, reply_markup=None):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
        resp = requests.get(self.api_url + method, params)
        return resp
