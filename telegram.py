# -*- coding: utf-8 -*-
import json
import requests

from proxy_tools import RotateProxy

from settings import TOKEN, CHAT_ID


class API:
    URL = 'https://api.telegram.org/bot{}/'

    def __init__(self, token=TOKEN, receiver_chat_id=CHAT_ID):
        self.token = token
        self.receiver_chat_id = receiver_chat_id
        self.bot_url = self.URL.format(self.token)

    def _get_url(self, url):
        proxies = RotateProxy()
        for proxy in proxies.iget_proxy():
            try:
                response = requests.get(url, proxies={"http": proxy, "https": proxy})
                content = response.content.decode("utf8")
                return content
            except:
                pass

    def _get_json_from_url(self, url):
        content = self._get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self):
        url = self.bot_url + "getUpdates"
        js = self._get_json_from_url(url)
        return js

    def _get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)

    def send_message(self, text):
        url = self.bot_url + "sendMessage?text={}&chat_id={}".format(text, self.receiver_chat_id)
        self._get_url(url)
