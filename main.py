# -*- coding: utf-8 -*-
import schedule
import time
import requests
import bs4

import netology
import telegram


CHECK_INTERVAL = 10


def check_hw():
    print('CHECKING NEW HOMEWORKS, RESULT:')
    api = netology.API()
    hw_list = api.get_homework_list()
    new_hw_list = [hw for hw in hw_list if not hw[4]]
    if new_hw_list:
        message = 'Новые домашки: \n'
        i = 1
        for hw in new_hw_list:
            message += '%s. %s: %s\n' % (i, hw[0], hw[1])
            i += 1
        tg_api = telegram.API()
        tg_api.send_message(message)
        print('MESSAGE ABOUT NEW HOMEWORKS SENDED:\n %s' % message)
    else:
        print('NO NEW HOMEWORKS')


def main():
    print('CHECKING HOMEWORKS STARTED, every %s min' % CHECK_INTERVAL)
    schedule.every(CHECK_INTERVAL).minutes.do(check_hw)
    check_hw()
    while True:
        schedule.run_pending()
        time.sleep(1)

main()
