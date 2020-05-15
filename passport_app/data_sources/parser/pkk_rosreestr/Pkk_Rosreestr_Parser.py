from passport_app.models import *
from passport_app.data_sources.parser.pkk_rosreestr.pkk_Rosreestr_Params import *

import requests
import json
import time
from urllib.parse import urlencode

REQ_TIMEOUT = 10

class Pkk_Rosreestr_Parser:
    def parse_data(self, real_estate: RealEstate):
        print ('START rosreestr.ru')

        params = {}
        # params = {
        #     'social': {}, 
        #     'transport': {}, 
        #     'place_info': {},
        #     'rights': {}, 
        #     'architecture': {},
        #     'engsys': {},
        #     'base': {}
        # }

        address = real_estate.latitude + ' ' + real_estate.longitude
        print('search for: ' + address)

        p = self.__get_data_from_pkk_by_address(address, params, real_estate.longitude + ' ' + real_estate.latitude)
        print(p)
        return p
        

    def __get_data_from_pkk_by_address(self, address, data_params, coordinates):
        json_content = None
        params = {
            '_' : str(int(time.time())),
            'text': address,
            'limit': '11',
            'skip': '0'
        }

        json_content = self.__load_page(params, 1)#участок
        if json_content:
            attrs = json_content['feature']['attrs']   
            #Вид
            data_params['ground_type'] = area_units[self.__get_value_or_empty(attrs, 'area_unit')]
            #Кадастровая стоимость
            data_params['ground_kadastr_cost'] = self.__get_value_or_empty(attrs, 'cad_cost')
            #Уточненная площадь
            data_params['ground_total_area'] = self.__get_value_or_empty(attrs, 'area_value')
            #Кадастровый номер
            data_params['ground_cn'] = self.__get_value_or_empty(attrs, 'cn')
            #Статус
            data_params['ground_status'] = self.__get_value_from_dict(states, self.__get_value_or_empty(attrs, 'statecd'))
            #Адрес
            data_params['ground_address'] = self.__get_value_or_empty(attrs, 'address')
            #Форма собственности
            data_params['ground_owning_form'] = ''
            #категория земель
            data_params['ground_category'] = self.__get_value_from_dict(category_types, self.__get_value_or_empty(attrs, 'category_type'))
            #Разрешённое использование
            data_params['ground_permitted_use'] = self.__get_value_from_dict(util_description, self.__get_value_or_empty(attrs, 'util_code'))
            #Разрешённое использование по документу
            data_params['ground_permitted_use_doc'] = self.__get_value_or_empty(attrs, 'util_by_doc')
            #Кадастровый номер квартала
            data_params['ground_kvartal_cn'] = self.__get_value_or_empty(attrs, 'kvartal_cn')

        json_content = self.__load_page(params, 5)#окс
        if json_content:
            attrs = json_content['feature']['attrs']

            #вид
            data_params['oks_type'] = self.__get_value_from_dict(oks_types, self.__get_value_or_empty(attrs, 'oks_type'))
            #Назначение
            data_params['oks_purpose'] = ''
            #Кадастровая стоимость
            data_params['oks_kadastr_cost'] = self.__get_value_or_empty(attrs, 'cad_cost')
            #Общая площадь
            data_params['oks_total_area'] = self.__get_value_or_empty(attrs, 'area_value')
            #общая этажность
            data_params['oks_floors'] = self.__get_value_or_empty(attrs, 'floors')
            #подземная этажность
            data_params['oks_underground_floors'] = self.__get_value_or_empty(attrs, 'underground_floors')
            #завершение строительства
            data_params['oks_year_built'] = self.__get_value_or_empty(attrs, 'year_built')
            #ввод в эксплуатацию
            data_params['oks_year_used'] = self.__get_value_or_empty(attrs, 'year_used')
            #Кадастровый номер
            data_params['oks_cn'] = self.__get_value_or_empty(attrs, 'cn')
            #Статус
            data_params['oks_status'] = self.__get_value_from_dict(states, self.__get_value_or_empty(attrs, 'statecd'))
            #Адрес
            data_params['oks_address'] = self.__get_value_or_empty(attrs, 'address')
            #Форма собственности
            data_params['oks_owning_form'] = ''
            #Кадастровый номер квартала
            data_params['oks_kvartal_cn'] = self.__get_value_or_empty(attrs, 'kvartal_cn')
        
        return data_params

    def __get_value_from_dict(self, _dict, key):
        try:
            return _dict[key]
        except (KeyError, TypeError):
            return ''

    def __get_value_or_empty(self, _dict, key):
        return _dict[key] if key in _dict else ''


    def __load_page(self, params, type):
        params['_'] = str(int(time.time()))
        url_params = urlencode(params)
        url_sttr = 'https://pkk.rosreestr.ru/api/features/' + str(type) + '?' + url_params
        try:
            response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
            data = response.text
            json_content = json.loads(data)
        except requests.Timeout:
            pass

        if not json_content or len(json_content['features']) == 0:
            print('nothing found')
            return {}

        # второй запрос, когда мы кликаем на найденный адресс
        try:
            search_number = json_content['features'][0]['attrs']['id']
            
            params['_'] = str(int(time.time()))
            url_params = urlencode(params)
            url_sttr = 'https://pkk.rosreestr.ru/api/features/' + str(type) + '/' + search_number
            response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
            json_content = json.loads(response.text)
        except (KeyError, TypeError, IndexError, requests.Timeout):  
            pass

        return json_content


    def __rosreestr_details_5kk(self, json_content, result):
        try:  # кадастровый инженер
            val = json_content['feature']['attrs']['cad_eng_data']['co_name']
            result['cadastral_engineer'] = val
        except (KeyError, TypeError):
            result['cadastral_engineer'] = ''

        try:  # кадастровый номер квартала
            val = json_content['feature']['attrs']['kvartal_cn']
            result['cadastral_number_of_the_block'] = val
        except (KeyError, TypeError):
            result['cadastral_number_of_the_block'] = ''

        try:  # категория земель
            val = category_types["%s" % json_content['feature']['attrs']['category_type']]
            result['land_category'] = val
        except (KeyError, TypeError):
            result['land_category'] = ''

        # try:  # категория земель (copy_of_passport_dc)
        #     result_content['category_of_land']['data'] = result_dc['land_category']['information']
        #     handleString(copy_of_passport_dc['category_of_land'])
        # except (KeyError, TypeError):
        #     pass

        try:  # Вид разрешённого использования
            val = util_description["%s" % json_content['feature']['attrs']['util_code']]
            result['permitted_use'] = val
        except (KeyError, TypeError):
            result['permitted_use'] = ''

        # try:  # Вид разрешённого использования (copy_of_passport_dc)
        #     copy_of_passport_dc['permitted_use']['data'] = result_dc['kind_of_permitted_use']['information']
        #     handleString(copy_of_passport_dc['permitted_use'])
        # except (KeyError, TypeError):
        #     pass

        try:  # Точность границ земельного участка
            val = json_content['feature']['extent']
            result['accuracy_of_land_boundaries'] = val
        except (KeyError, TypeError):
            result['accuracy_of_land_boundaries'] = ''

        # try:  # Точность границ земельного участка (copy_of_passport_dc)
        #     copy_of_passport_dc['accuracy_of_land_boundaries']['data'] = \
        #     result_dc['the_accuracy_of_the_boundaries_of_the_land']['information']
        # except (KeyError, TypeError):
        #     pass

        try:  # данные кадастрового паспорта земельного участка
            val = json_content['feature']['attrs']['util_by_doc']
            result['data_of_the_cadastral_passport_of_the_land_plot'] = val
        except (KeyError, TypeError):
            result['data_of_the_cadastral_passport_of_the_land_plot'] = ''

        # try:  # кадастровая стоимость здания
        #     result_content['cadastral_value_of_the_building'] = str(
        #         json_content['feature']['attrs']['cad_cost']) + ' руб'
        # except (KeyError, TypeError):
        #     result_content['cadastral_value_of_the_building'] = ''

        try:  # дата постановки на кадастровый учёт
            val = json_content['feature']['attrs']['date_create']
            result['date_of_cadastral_registration'] = val
        except (KeyError, TypeError):
            result['date_of_cadastral_registration'] = ''

        try:  # год постройки
            val = json_content['feature']['attrs']['year_built']
            result['year_of_construction'] = val
        except (KeyError, TypeError):
            result['year_of_construction'] = ''

        try:  # год ввода в эксплуатацию
            val = json_content['feature']['attrs']['year_used']
            result['year_of_commissioning'] = val
        except (KeyError, TypeError):
            result['year_of_commissioning'] = ''

        try:  # общая площадь
            val = json_content['feature']['attrs']['area_value']
            result['total_area'] = val
        except (KeyError, TypeError):
            result['total_area'] = ''

        try:  # этажность
            val = json_content['feature']['attrs']['floors']
            result['number_of_storeys'] = val
        except (KeyError, TypeError):
            result['number_of_storeys'] = ''

        try:  # подземных этажей
            val = json_content['feature']['attrs']['underground_floors']
            result['underground_floors'] = val
        except (KeyError, TypeError):
            result['underground_floors'] = ''

        # try:  # Площадь застройки (для copy_of_passport_dc)
        #     copy_of_passport_dc['building_area']['data'] = \
        #         json_content['feature']['attrs']['area_dev']
        #     handleString(copy_of_passport_dc['building_area'])
        # except (KeyError, TypeError, AttributeError):
        #     pass

        # try:  # Функциональное назначение объекта капитального строительства
        #     result_content['functional_purpose_of_the_capital_construction_object'] = json_content['feature']['attrs']['name']
        # except (KeyError, TypeError):
        #     result_content['functional_purpose_of_the_capital_construction_object'] = ''

        return result