import requests
from bs4 import BeautifulSoup
import time
import json
import random

class Avito_Parser():
    def pase_data(self, address):
        print("start AVITO")
        result = {}

        data = self.__parse("https://www.avito.ru/rossiya/komnaty/prodam-ASgBAgICAUSQA74Q?q=" + address)
        result['buy_part_apartment Avito'] = self.__calc_average_price(data)
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/prodam/1-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?q=" + address)
        result['buy_1_room Avito'] = self.__calc_average_price(data)
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/prodam/2-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?q=" + address)
        result['buy_2_room Avito'] = self.__calc_average_price(data)
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/prodam/3-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?q=" + address)
        result['buy_3_room Avito'] = self.__calc_average_price(data)
        data = self.__parse("https://www.avito.ru/rossiya/kvartiry/prodam/4-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?q=" + address)
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
        counter = 2
        r = requests.get(url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.129'})
        print('!!__!!')
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
    
        lincs = soup('div', class_="styles-root-2nfT7")
        
        data = []
        for linc in lincs:
            link = 'https://www.avito.ru' + str(linc.find('a', class_='link-link-39EVK').get('href'))
            print(link)
            get_request = requests.get(link, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.129'})
            html = get_request.text 
            content = BeautifulSoup(html, 'html.parser')
            
            title = str(content.find('span', class_='title-info-title-text'))
            title = title.replace('<span class="title-info-title-text" itemprop="name">', '')
            title = title.replace('</span>', '')
            print(title)
            price = str(content.find('span', class_='js-item-price').get('content'))
            print(price)
            locate = content.find('span', class_='item-address__string')
            locate = str(locate).replace('<span class="item-address__string">', '')
            locate = str(locate).replace('</span>', '')
            print(locate)
            radiuses = content('li', class_='item-params-list-item')
            rr = ''
            for r in radiuses:
                radius = str(str(r).replace('<li class="item-params-list-item"> <span class="item-params-label">', ' '))
                radius = str(str(radius).replace('</span>', ' '))
                radius = str(str(radius).replace('</li>', ' '))
                rr += radius
            print(rr)
            names = content.find('div', class_='seller-info-name')
            name = names.find('a')
            href_name = name.get('href')
            
            shifer = '<a href="' + str(href_name) + '" title="Нажмите, чтобы перейти в профиль">'
            name = str(str(name).replace(shifer, ''))
            name = str(str(name).replace('</a>', ''))
            name = name[-30:]
            print(name)
            
            with open('data.json', 'r', encoding='utf-8') as f:  
                try:
                    data = json.load(f)
                except:
                    data = []
                f.close()
            
            object = {
                'Price': price,
                'Location': str(locate),
                'Name': name,
                'Radius': rr,
                'Title': title,
                'Link': str(link)
            }
            data.append(object)
            
            time.sleep(random.randint(5, 8))
        
        return data

