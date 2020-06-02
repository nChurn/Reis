import requests
from bs4 import BeautifulSoup
import time
import json
import random

class Cian_Parser():
    def parse_data(self, address):
        run = True
        pagenator = 1
        while run:          
            with open('cian.json', 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except:
                    data = []
                f.close()
                    
            print('!_!_!')
            r = requests.get(f'https://www.cian.ru/cat.php?deal_type=rent&engine_version=3&offer_type=flat&p={pagenator}&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1&type=4',
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.129'})
            print(f'Страница: {pagenator}')
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
                    print('was replaced:')
                    
                    
                print(title)
                
                
                #-------#
                price = content.find('div', class_='c6e8ba5398--header--1dF9r')
                price = str(price).replace('<div class="c6e8ba5398--header--1dF9r">', '')
                price = str(price).replace('</div>', '')
                print(price)
                object = {
                    'title': title,
                    'price': price
                }
                
                data.append(object)
            
            with open('cian.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
                f.close()
            time.sleep(random.randint(5,8))