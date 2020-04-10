import json
import logging

import requests

from passport_app.email_manager import send_error
from passport_app.models import *
from passport_app.print_exception import *

logger = logging.getLogger(__name__)

class YandexMapsAPI:
    __real_estate : RealEstate
    api_key = ''
    places_api_key = 'c687c609-ae0e-4b12-8d9a-aab953d8642f'
    is_send_email = False

    def __init__(self, real_estate: RealEstate, api_key, places_api_key, is_send_email):
        self.__real_estate = real_estate
        self.api_key = api_key
        self.is_send_email = is_send_email
        self.places_api_key = places_api_key

    def parse_info(self, lang_code):
        result = {}

        print("START yandex search")
        address_result = self.get_address_data(address = self.__real_estate.address)
        address_point = address_result['point'].split(' ')
        lat = address_point[0]
        lng = address_point[1]
        print("yandex search coord: " + address_result['point'])

        social_infr = ParserParameter.objects.filter(parser_parameter_type='social', parser_type_id = 3)
        transport_dist = ParserParameter.objects.filter(parser_parameter_type='transport_dist', parser_type_id = 3)

        for item in social_infr:
            try:
                count = self.__get_near_places(lat = lat, lng = lng, place = item.name_ru)
                            
                result[item.name] = count
                self.__save_to_parameter_data(item, str(count))
            except Exception as e:
                if self.is_send_email:
                    send_error(str(e))
                PrintException()
                #__save_to_parameter_data(real_estate, item, str(0), is_send_email=True)
        
        for item in transport_dist:
            try:
                count = self.__get_near_places(lat = lat, lng = lng, place = item.name_ru)
                            
                result[item.name] = count
                self.__save_to_parameter_data(item, str(count) + ' dist')
            except Exception as e:
                if self.is_send_email:
                    send_error(str(e))
                PrintException()
                #__save_to_parserparameter_data(real_estate, item, str(0), is_send_email=True)

        return result

    def get_address_data(self, address):
        url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey=%s&geocode=%s&results=1' % (self.api_key, address)
        response = requests.get(url)

        country = ''
        province = ''
        province2 = ''
        locality = ''
        street = ''
        house = ''
        text_address = ''
        point = ''

        try:
            if response.status_code == 200:
                json_data = json.loads(response.text)
                geo_metadata = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components']

                for address_itmes in geo_metadata:
                    if address_itmes['kind'] == 'country':
                        country = address_itmes['name']

                    if address_itmes['kind'] == 'province' and province == '':
                        province = address_itmes['name']
                    elif address_itmes['kind'] == 'province':
                        province2 = address_itmes['name']

                    if address_itmes['kind'] == 'locality':
                        locality = address_itmes['name']

                    if address_itmes['kind'] == 'street':
                        street = address_itmes['name']

                    if address_itmes['kind'] == 'house':
                        house = address_itmes['name']

                text_address = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                point_tmp = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')

                point = point_tmp[1] + " " + point_tmp[0]
        except Exception as e:
            if self.is_send_email:
                send_error(str(e))
            PrintException()

        result = {
            "country": country,
            "province": province,
            "province2":province2,
            "locality":locality,
            "street": street,
            "house": house,
            "text_address": text_address,
            "point": point
        }

        return result

    def __get_near_places(self, lat, lng, place):
        print("start __get_near_places")
        distance_lat = 0.016667
        distance_lng = 0.016667

        place = place.replace('Yandex', '')

        url = 'https://search-maps.yandex.ru/v1/?text=%s&ll=%.6f,%.6f&spn=%.6f,%.6f&lang=ru_RU&apikey=%s' % \
            (place, float(lat), float(lng), float(distance_lat), float(distance_lng), self.places_api_key)
        response = requests.get(url)
        print(response.status_code)
        try:
            if response.status_code == 200:
                json_data = json.loads(response.text)
                # features = json_data['features']
                # len_features = len(features)
                
                len_features = json_data['properties']['ResponseMetaData']['SearchResponse']['found']

                return len_features            
        except Exception as e:
            if self.is_send_email:
                send_error(str(e))
                PrintException()

        return 0

    def __save_to_parameter_data(self, parser_parameter, value):
        parser_parameter = ParserParameter.objects.get(name = parser_parameter.name)
        
        try:
            parameter = Parameter.objects.get(name_ru = parser_parameter.name_ru.replace('Yandex', '').strip())
            parameter_data = ParameterData()

            parameter_data.value = value
            parameter_data.real_estate = self.__real_estate
            parameter_data.parameter = parameter
            parameter_data.comment = 'yandex'
            parameter_data.save()
        except Exception as e:
            logger.error('Parameter not found in db:' + parser_parameter.name)
            