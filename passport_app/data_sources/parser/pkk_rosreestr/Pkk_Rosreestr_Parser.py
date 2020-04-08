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

        address = real_estate.longitude + ' ' + real_estate.latitude
        print('search for: ' + address)

        p = self.__get_data_from_pkk_by_address(address, params, real_estate.longitude + ' ' + real_estate.latitude)
        print(p)
        return p
        

    def __get_data_from_pkk_by_address(self, address, data_params, coordinates):
        json_content = None
        params = {
            '_' : str(int(time.time())),
            'text': address,
            'limit': '11',  # лимит ответов, мы берем всегда первый
            'skip': '0'
        }

        url_params = urlencode(params)
        type = 5
        url_sttr = 'https://pkk.rosreestr.ru/api/features/' + str(type) + '?' + url_params
        try:
            response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
            data = response.text
            json_content = json.loads(data)
        except requests.Timeout:
            pass

        if not json_content or len(json_content['features']) == 0:
            print('nothing found')
            return data_params

        # второй запрос, когда мы кликаем на найденный адресс
        try:
            search_number = json_content['features'][0]['attrs']['id']  # типо кадастрового номера только без нулей
            
            params['_'] = str(int(time.time()))
            url_params = urlencode(params)
            url_sttr = 'https://pkk.rosreestr.ru/api/features/' + str(type) + '/' + search_number
            response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
            json_content = json.loads(response.text)
        except (KeyError, TypeError, IndexError, requests.Timeout):  # когда переход на адресс не удался
            pass

        attrs = json_content['feature']['attrs']
        data_params['address'] = attrs['address']
        #Кадастровый номер помещения
        data_params['kadastr_number'] = attrs['cn']
        #Общая площадь помещения, м2
        data_params['total_area'] = attrs['area_value']
        #Кадастровая стоимость помещения, рублей
        data_params['kadastr_cost'] = attrs['cad_cost'] if 'cad_cost' in attrs else ''
        #Год постройки
        data_params['year_built'] = attrs['year_built'] if 'year_built' in attrs else ''
        #Год ввода в эксплуатацию
        data_params['year_in_used'] = attrs['year_used'] if 'year_used' in attrs else ''
        
        self.__rosreestr_details_5kk(json_content, data_params)


        type = 1
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
            print('nothing found plot')
            return data_params
        # второй запрос, когда мы кликаем на найденный адресс
        try:
            search_number = json_content['features'][0]['attrs']['id']  # типо кадастрового номера только без нулей
            
            params['_'] = str(int(time.time()))
            url_params = urlencode(params)
            url_sttr = 'https://pkk.rosreestr.ru/api/features/' + str(type) + '/' + search_number
            response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
            json_content = json.loads(response.text)
        except (KeyError, TypeError, IndexError, requests.Timeout):  # когда переход на адресс не удался
            pass

        attrs = json_content['feature']['attrs']   
        data_params['address'] = attrs['address']
        #Кадастровый номер земельного участка
        data_params['plot_kadastr_number'] = attrs['cn']
        #Общая площадь помещения земельного участка, м2
        data_params['plot_total_area'] = attrs['area_value']        

        return data_params

    def __parse_json_params(self, json_data, result):
        attrs = json_data['feature']['attrs']

        result['address'] = attrs['address']
        #Кадастровый номер помещения
        result['kadastr_number'] = attrs['cn']
        #Общая площадь помещения, м2
        result['total_area'] = attrs['area_value']
        #Кадастровая стоимость помещения, рублей
        result['kadastr_cost'] = attrs['cad_cost'] if 'cad_cost' in attrs else ''
        #Год постройки
        result['year_built'] = attrs['year_built'] if 'year_built' in attrs else ''
        #Год ввода в эксплуатацию
        result['year_in_used'] = attrs['year_used'] if 'year_used' in attrs else ''
        #Кадастровый номер земельного участка
        #...


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