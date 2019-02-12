# -*- coding: utf-8 -*-
import bs4
import requests

import settings


class API:
    LOGIN_URL = 'https://netology.ru/backend/admin/sign_in'
    LOGIN_POST_URL = LOGIN_URL
    ACCOUNT_URL = 'https://netology.ru/backend/admin'
    HOMEWORK_LIST_URL = 'https://netology.ru/backend/admin/tasks/homeworks'

    def __init__(self, user_login = settings.login, user_password = settings.password):
        self.user_login = user_login
        self.user_password = user_password
        self.authenticity_token, self.cookies = self.login()

    def login(self):
        login_page = requests.get(self.LOGIN_URL)
        authenticity_token = self._extract_authenticity_token(login_page.text)
        params = {'utf8': '%E2%9C%93',
                  'authenticity_token': authenticity_token,
                  'admin[email]': self.user_login,
                  'admin[password]': self.user_password,
                  'commit': '%D0%92%D0%BE%D0%B9%D1%82%D0%B8',
                  }

        account_page = requests.post(self.LOGIN_POST_URL, params, cookies=login_page.cookies)
        cookies = account_page.cookies

        return authenticity_token, cookies

    def is_login(self):
        account_page = requests.get(self.ACCOUNT_URL, cookies=self.cookies)
        return True if account_page.status_code ==200 else False

    def logout(self):
        pass

    def get_account(self):
        pass

    def get_homework_list(self):
        list_page = requests.get(self.HOMEWORK_LIST_URL, cookies=self.cookies)
        soup = bs4.BeautifulSoup(list_page.text)
        strings = soup.find('table').find('tbody').findAll('tr')
        hw_list = []
        for hw in strings[1:]:
            hw_params = [hw_param.text for hw_param in hw.findAll('td')]
            hw_list.append(hw_params)
        return hw_list

    def _extract_authenticity_token(self, text):
        try:
            soup = bs4.BeautifulSoup(text)
            token = soup.find(attrs={'name': 'authenticity_token', })
            return token['value']
        except Exception as e:
            pass # logs