import requests
from bs4 import BeautifulSoup
import time
import json
import random

class Avito_Parser():
    def pase_data(self, address):
        print("start AVITO")
        counter = 2
        
        r = requests.get('https://www.avito.ru/ekaterinburg/nedvizhimost', 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.129'})
        print('!!__!!')
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
    
        lincs = soup('div', class_="styles-root-2nfT7")
        
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
                'Nedvizhimost':{
                    'Price': price,
                    'Location': str(locate),
                    'Name': name,
                    'Radius': rr,
                    'Title': title,
                    'Link': str(link)
                }
            }
            data.append(object)
            
            time.sleep(random.randint(5, 8))
        
        return data

