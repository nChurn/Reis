from datetime import datetime

import os
from pyquery import PyQuery as pq, PyQuery
# from estp.items import result
import uuid
from urllib.request import urlopen

import codecs
from datetime import datetime
from urllib.parse import urlencode
# from grab import Grab
import requests
from bs4 import BeautifulSoup

import html

test_search_words = [
u'Атмосфера,  воздух', 
u'Водные ресурсы, вода'
u'Земельные ресурсы, почва',
u'ООПТ',
u'Биоразнообразние',
u'Биоресурсы',
u'Климат',
u'Природо-охранный индекс']

def __getOkrugName(okrug):
    if "Смоленская":
        return 'smolenskaya-oblast'
    return 'smolenskaya-oblast'

def __handle_content(soup, key_words):
    result = {}
    for key_item in key_words:        
        div_with_text = soup.find("div", text=key_item)
        print(div_with_text)
        if div_with_text:
            rate = div_with_text.parent.parent.find('div', {'class':'.field-indx-rates'})
            print(div_with_text.parent.parent.findChildren())
            result[key_item] = rate
            print(rate)
    return result

def search(okrug):

    print("green patrol okrug:"+okrug)
    okrug_name = __getOkrugName(okrug)
    url = 'https://greenpatrol.ru/ru/regiony/'+okrug_name
    print("green patrol url:"+url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = __handle_content(soup, test_search_words)
    return result
