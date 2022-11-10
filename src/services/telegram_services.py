import requests


class TelegramServices:

    def send_message(self, chat_id: str, token: str, content: str):
        apiURL = f'https://api.telegram.org/bot{token}/sendMessage'

        try:
            return requests.post(apiURL, json={'chat_id': chat_id, 'text': content})
        except Exception as e:
            print(e)
