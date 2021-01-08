# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 14:59:08 2020

@author: kary
"""


def telegram_send_text(text):
    import telegram
    TOKEN='*********************************************'
    bot=telegram.Bot(TOKEN)
    chat_id=bot.get_updates()[-1].message.chat_id
    bot.send_message(chat_id, text)
    
def telegram_send_image(local_path):
    import requests
    import telegram
    TOKEN='***********************************************'
    bot=telegram.Bot(TOKEN)
    send_to_user_id=bot.get_updates()[-1].message.chat_id
    requests.post(bot.base_url + '/sendPhoto', data={'chat_id': send_to_user_id}, files={'photo': open(local_path, 'rb')})
    
    