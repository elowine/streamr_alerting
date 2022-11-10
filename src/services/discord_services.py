import requests as rq


class DiscordServices:

    def _auths(self, token: str) -> dict:
        return {
            'authorization': token
        }

    def _message(self, content: str) -> dict:
        return {
            'content': content
        }

    def send_message(self, id_channel: str, token: str, content: str):
        try:
            url = f"https://discord.com/api/v9/channels/{id_channel}/messages"
            auth = self._auths(token)
            msg = self._message(content)

            return rq.post(url, headers=auth, data=msg).json()
        except Exception as e:
            print(e)
