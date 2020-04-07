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
import re

def search_by_cn(cn, contains):
    cn_formated = cn.replace(':', '-')
    url = 'https://rosreestr.net/kadastr/' + cn_formated
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:  # получить ссылку из блока с результатами
        cn_divs = soup.find_all("div", text= re.compile("^Кадастровый номер: *"))
        print(cn_divs)
        for cn_div in cn_divs:
            cn_str = cn_div.getText().replace('Кадастровый номер: ', '')
            if cn_str:
                contains['base']['kadastr_number'] = cn_str[1:]

    except TypeError:  # если в поиске найдено 0 результато
        pass

    try:
        address_div = soup.find('div', text = re.compile("^Адрес по документам: *"))
        print(address_div)
        contains['base']['address'] = address_div.getText().replace('Адрес по документам: ', '')
    except TypeError:  # если в поиске найдено 0 результато
        pass


