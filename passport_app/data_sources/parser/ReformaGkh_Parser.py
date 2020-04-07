import time
from selenium import webdriver
from datetime import datetime

import os
from pyquery import PyQuery as pq, PyQuery
import uuid
from urllib.request import urlopen

import codecs
from datetime import datetime
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from passport_app.models import *
import json
import logging

logger = logging.getLogger(__name__)

class ReformaGkh_Parser():
    table_field_keys = {
        'year_building':'Год постройки:', 
        'year_of_commissioning':'Год ввода дома в эксплуатацию:',
        'series_building_type':'Серия, тип постройки здания:',
        'type_of_house':'Тип дома:',
        'method_of_formation_of_the_capital_repair_fund':'Способ формирования фонда капитального ремонта:',
        'the_house_is_recognized_as_an_emergency':'Дом признан аварийным:',
        'most_floors':'наибольшее, ед.',
        'fewest_floors':'наименьшее, ед.',
        'number_of_entrances':'Количество подъездов, ед.',
        'number_of_elevators':'Количество лифтов, ед.',
        'number_of_common_premises':'общее, ед.',
        'number_of_residential_premises':'жилых, ед.',
        'number_of_unresidential_premises':'нежилых, ед.',
        'total_area_common_premises':'общая площадь, кв.м',
        'total_area_of_​​living_quarters':'общая площадь жилых помещений, кв.м',
        'total_area_of_​​non_residential_premises':'общая площадь нежилых помещений, кв.м',
        'total_area_of_​​premises_included_in_the_total_property':'общая площадь помещений, входящих в состав общего имущества, кв.м',

        'the_area_of_​​the_land_plot':'площадь земельного участка, входящего в состав общего имущества в многоквартирном доме, кв.м',
        'area_of_​​parking_within_the_boundaries_of_the_land_plot':'площадь парковки в границах земельного участка, кв.м',
        'cadastral_number_of_the_building':'Кадастровый номер',
        'energy_efficiency_class':'Класс энергетической эффективности:',
        'gkh_playground':'детская площадка',
        'gkh_sportground':'спортивная площадка',
        'gkh_other':'другое',
        'additional_information_about_the_property':'Дополнительная информация:',

        'type_of_foundation': 'Тип фундамента',
        'floor_type':'Тип перекрытий',
        'material_of_bearing_walls':'Материал несущих стен',
        'basement_area':'Площадь подвала по полу, кв.м',
        'type_of_garbage_chute':'Тип мусоропровода',
        'number_of_garbage_chutes':'Количество мусоропроводов, ед.',

        'type_of_power_supply_system':'Тип системы электроснабжения',
        'number_of_entries_in_the_house':'Количество вводов в дом, ед.',
        'type_of_heat_supply_system':'Тип системы теплоснабжения',
        'type_of_hot_water_system':'type_of_hot_water_system',
        'type_of_cold_water_supply_system':'Тип системы холодного водоснабжения',
        'type_of_sewerage_system':'Тип системы водоотведения',
        'volume_of_cesspools':'Объем выгребных ям, куб. м.',
        'type_of_gas_supply_system':'Тип системы газоснабжения',
        'type_of_ventilation_system':'Тип системы вентиляции',
        'type_fire_extinguishing_system':'Тип системы пожаротушения',
        'gutter_system_type':'Тип системы водостоков',
    }

    lift_data_keys = {
        '':'',
        '':'',
        '':'',
    }

    fundament_data_keys = {

    }

    def parse_data(self, address, real_estate):
        print ('start reformagkh.ru')
        print('search address: ' + address)

        address_str = real_estate.district_name+", " + real_estate.locality_name + ", " + real_estate.street_name + ", " + real_estate.house_number
        print("address_str= " + address_str)
        params = {
            'all': 'on',
            'query': address_str
        }

        url_params = urlencode(params)
        url = 'https://www.reformagkh.ru/search/houses-autocomplete?query=' + url_params
        print("GKH  autocomplete url:"+url)
        page = requests.get(url)
        json_content = json.loads(page.text)
        print ("autocomplete result : ")
        print (json_content)

        search_address = address
        if json_content and json_content['addresses']:
            search_address = json_content['addresses'][0]

        print("GKH address:"+search_address)
        result = {}
        params = {'all': 'on',
                'query': search_address}
        url_params = urlencode(params)
        url = 'https://www.reformagkh.ru/search/houses' + '?' + url_params
        print("GKH url:"+url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        try:  # получить ссылку из блока с результатами
            if soup.find('table'):
                house_link = 'https://www.reformagkh.ru' + soup.find('table').find('a', href=True)['href']
                page = requests.get(house_link)
                soup = BeautifulSoup(page.content, 'html.parser')            
                result = self.__get_data_by_address(soup)  # записываем контет в массивы
        except TypeError:  # если в поиске найдено 0 результатов
            result = {}        

        self.__save_info_to_db(result, real_estate)
        return result

    def __get_data_by_address(self, soup):
        result = {}
        try:
            el = soup.body.find('div', text='Площадь дома:').parent
            el_val = el.find_all('div', recursive=False)[-1]
            if el_val:
                result['gkh_square_house'] = el_val.getText()   
        except (KeyError, TypeError, AttributeError):
            pass

        try:
            el = soup.body.find('div', text='Этажей:').parent
            el_val = el.find_all('div', recursive=False)[-1]
            if el_val:
                result['gkh_floors'] = el_val.getText()
        except (KeyError, TypeError, AttributeError):
            pass

        self.__get_data_from_table(soup, self.table_field_keys, result)
        return result

    def __get_data_from_table(self, soup, field_keys, result):
        for field_item in field_keys:
            field_key = field_keys[field_item]
            try:
                el = soup.body.find('td', text=field_key).parent
                el_val = el.find_all('td', recursive=False)[-1]
                if el_val:
                    result[field_item] = el_val.getText()   
            except (KeyError, TypeError, AttributeError):
                pass    
            

    def __save_info_to_db(self, result,  real_estate):
        for item_key in result:
            try:
                parser_parameter = ParserParameter.objects.get(name = item_key)

                parameter = Parameter.objects.get(name_ru = parser_parameter.name_ru)
                parameter_data = ParameterData()

                parameter_data.value = result[item_key]
                parameter_data.real_estate = real_estate
                parameter_data.parameter = parameter
                parameter_data.save()
            except Exception as e:
                logger.error(item_key)
                logger.error(str(e))
                pass