import json
import random
import time
import re

import requests
from lxml import html


class Avito_Parser():
    def pase_data(self, address):
        print("start AVITO")
        result = {}
        address = address.replace('Россия, ', '')

        data = self.__parse("https://www.avito.ru/rossiya/komnaty/prodam-ASgBAgICAUSQA7wQ?q=" + address)
        result['buy_part_apartment Avito'] = self.__calc_average_price(data)
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/prodam/1-komnatnye-ASgBAQICAUSSA8YQAUDKCBSAWQ?q=" + address)
        result['buy_1_room Avito'] = self.__calc_average_price(data)
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/prodam/2-komnatnye-ASgBAQICAUSSA8YQAUDKCBSAWQ?q=" + address)
        result['buy_2_room Avito'] = self.__calc_average_price(data)
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/prodam/3-komnatnye-ASgBAQICAUSSA8YQAUDKCBSAWQ?q=" + address)
        result['buy_3_room Avito'] = self.__calc_average_price(data)
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/prodam/4-komnatnye-ASgBAQICAUSSA8YQAUDKCBSAWQ?q=" + address)
        result['buy_4_room Avito'] = self.__calc_average_price(data)

        data = self.__parse("https://www.avito.ru/rossiya/komnaty/sdam-ASgBAgICAUSQA74Q?q=" + address)
        result['year_rent_part_apartment Avito'] = self.__calc_average_price(data) * 12
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/sdam/1-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?q=" + address)
        result['year_rent_1_room Avito'] = self.__calc_average_price(data) * 12
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/sdam/2-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?q=" + address)
        result['year_rent_2_room Avito'] = self.__calc_average_price(data) * 12
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/sdam/3-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?q=" + address)
        result['year_rent_3_room Avito'] = self.__calc_average_price(data) * 12
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/sdam/4-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?q=" + address)
        result['year_rent_4_room Avito'] = self.__calc_average_price(data) * 12

        return result
        
    def __calc_average_price(self, info):
        if len(info) == 0:
            return 0
        return sum(float(x['price']) for x in info) / len(info)


    def __parse(self, url):
        result = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.129'
        }

        page_number = 1
        while page_number != -1:  
            print("page: " + str(page_number))
            page_query = ''
            if page_number > 1:
                page_query = '&p={}' % page_number

            time.sleep(random.randint(5, 8))

            r = requests.get(url + page_query, headers=headers)
            html_doc = html.fromstring(r.text)  

            links = html_doc.xpath("//div[contains(@class, 'snippet-list')]/div[contains(@class, 'item')]")
            for link in links:
                price_node = link.xpath(".//span[contains(@class, 'snippet-price')]")
                text = price_node[0].text.replace(' ', '')
                num = re.search(r'\d+', text)

                result.append({
                    'price': float(num.group(0))
                })

            page_number = page_number + 1
            check = html_doc.xpath("//span[@data-marker = 'page({page_number})']")
            if check is None or len(check) == 0:
                page_number = -1
        
        return result
