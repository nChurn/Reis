import json
import random
import time

import requests
from bs4 import BeautifulSoup
from lxml import html

from passport_app.models import RealEstate


class Cian_Parser():
    def pase_data(self, real_estate: RealEstate):
        print("start Cian")
        result = {}        
        address_id = self.__get_address_id(real_estate)

        data = self.__parse("https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&house[0]={address_id}&offer_type=flat&room0=1")
        result['buy_part_apartment Avito'] = self.__calc_average_price(data)
        data = self.__parse("https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&house[0]={address_id}&offer_type=flat&room1=1")
        result['buy_1_room Cian'] = self.__calc_average_price(data)
        data = self.__parse("https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&house[0]={address_id}&offer_type=flat&room2=1")
        result['buy_2_room Cian'] = self.__calc_average_price(data)
        data = self.__parse("https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&house[0]={address_id}&offer_type=flat&room3=1")
        result['buy_3_room Cian'] = self.__calc_average_price(data)
        data = self.__parse("https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&house[0]={address_id}&offer_type=flat&room4=1")
        result['buy_4_room Cian'] = self.__calc_average_price(data)

        data = self.__parse("https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&house[0]={address_id}&offer_type=flat&room0=1")
        result['year_rent_part_apartment Cian'] = self.__calc_average_price(data) * 12
        data = self.__parse("https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&house[0]={address_id}&offer_type=flat&room1=1")
        result['year_rent_1_room Cian'] = self.__calc_average_price(data) * 12
        data = self.__parse("https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&house[0]={address_id}&offer_type=flat&room2=1")
        result['year_rent_2_room Cian'] = self.__calc_average_price(data) * 12
        data = self.__parse("https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&house[0]={address_id}&offer_type=flat&room3=1")
        result['year_rent_3_room Cian'] = self.__calc_average_price(data) * 12
        data = self.__parse("https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&house[0]={address_id}&offer_type=flat&room4=1")
        result['year_rent_4_room Cian'] = self.__calc_average_price(data) * 12

        return result
        
    def __calc_average_price(self, info):
        if len(info) == 0:
            return 0
        return sum(float(x['price']) for x in info) / len(info)

    def __get_address_id(self, real_estate):
        post_data = {
            'Address': real_estate.address,
            'Kind': 'house',
            'Lat': real_estate.latitude,
            'Lng': real_estate.longitude
        }

        resp = requests.post("https://www.cian.ru/api/geo/geocoded-for-search/", post_data)
        json_obj = json.loads(resp.text)

        return [x['id'] for x in json_obj['details'] if x['geoType'] == 'House'][0]

    def __parse(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.129'
        }
        run = True
        pagenator = 1
        data = []
        while run:                      
            print('!_!_!')
            time.sleep(random.randint(5,8))
            r = requests.get(url + '&p={pagenator}', headers=headers)
            html = r.text
            pagenator += 1
            
            #parsing 
            soup = BeautifulSoup(html, 'html.parser')
            block = soup('div', class_='_93444fe79c--card--_yguQ')
            
            for content in block:
                title = content.find('div', class_='c6e8ba5398--single_title--22TGT')
                title = str(title).replace('<div class="c6e8ba5398--single_title--22TGT" data-name="TopTitle">', '')
                title = str(title).replace('</div>', '')
                if title == 'None' or title is None:
                    title = content.find('div', class_='c6e8ba5398--subtitle--UTwbQ')
                    title = str(title).replace('<div class="c6e8ba5398--subtitle--UTwbQ">', '')
                    title = str(title).replace('</div>', '')
                    
                #-------#
                price = content.find('div', class_='c6e8ba5398--header--1dF9r')
                price = str(price).replace('<div class="c6e8ba5398--header--1dF9r">', '')
                price = str(price).replace('</div>', '')

                text = price.replace(' ', '')
                num = re.search(r'\d+', text)
                obj = {
                    'title': title,
                    'price': float(num.group(0))
                }
                
                data.append(obj)
            
            html_doc = html.loads(r.text)
            check = html_doc.xpath("//div[@data-name = 'Pagination']//span[text() = '{pagenator}']")
            if check is None or len(check) == 0:
                run = False
        
        return data
