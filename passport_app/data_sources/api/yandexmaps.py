import requests
from passport_app.email_manager import send_error
import json
from passport_app.models import *
import logging
from passport_app.print_exception import *

logger = logging.getLogger(__name__)

def __get_distance_places(apiKey, address):
    url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey=%s&geocode=%s' % (apiKey, address)
    response = requests.get(url)


def __yandex_get_address_data(apiKey, address, is_send_email = False):
    url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey=%s&geocode=%s&results=1' % (apiKey, address)
    response = requests.get(url)
    logger.error(response.status_code)

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
        if is_send_email:
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

def __save_to_parserparameter_data(real_estate, _parser_parameter, value, is_send_email = False):
    try:
        parser_parameter = ParserParameter.objects.filter(name_ru = _parser_parameter.name_ru).first()

        parameter = Parameter.objects.filter(name_ru = parser_parameter.name_ru).first()
        parameter_data = ParameterData()

        parameter_data.value = value
        parameter_data.real_estate = real_estate
        parameter_data.parameter = parameter
        parameter_data.save()
    except Exception as e:
        logger.error(str(_parser_parameter.id) + ' Parameter not found in db: ' + _parser_parameter.name_ru)

def __save_to_parameter_data(real_estate, parser_parameter, value, is_send_email = False):
    parser_parameter = ParserParameter.objects.get(name = parser_parameter.name)
    
    try:
        parameter = Parameter.objects.get(name_ru = parser_parameter.name_ru)
        parameter_data = ParameterData()

        parameter_data.value = value
        parameter_data.real_estate = real_estate
        parameter_data.parameter = parameter
        parameter_data.comment = 'yandex'
        parameter_data.save()
    except Exception as e:
        logger.error('Parameter not found in db:' + parser_parameter.name)
        logger.error(str(e))

def __get_near_places(apiKey, lat, lng, place, distance, is_send_email = False):
    logger.error("start __get_near_places")

    url = 'https://search-maps.yandex.ru/v1/?text=%s&ll=%.6f,%.6f&spn=%.6f,%.6f&lang=ru_RU&apikey=%s' % \
        (place, float(lat), float(lng), float(distance), float(distance), 'c687c609-ae0e-4b12-8d9a-aab953d8642f')
    response = requests.get(url)
    logger.error("__get_near_places")
    logger.error(response.status_code)
    
    try:
        if response.status_code == 200:
            json_data = json.loads(response.text)
            features = json_data['features']
            len_features = len(features)
            
            return len_features            
    except Exception as e:
        if is_send_email:
            send_error(str(e))
            PrintException()

    return 0

def yandex_search(keyAPI, address, real_estate, social_infr, transport_dist, lang_code, is_send_email = False):
    print("START yandex search")
    address_result = __yandex_get_address_data(apiKey = keyAPI, address = address, is_send_email=True)
    address_point = address_result['point'].split(' ')
    lat = address_point[0]
    lng = address_point[1]
    print("yandex search coord")
    print(address_result['point'])
    result = {}

    for item in social_infr:
        try:
            count = __get_near_places(apiKey = keyAPI, lat = lat, lng = lng, place = item.name_ru, distance = 1.00)
                        
            result[item.name] = count
            __save_to_parameter_data(real_estate, item, str(count), is_send_email=True)
        except Exception as e:
            if is_send_email:
                send_error(str(e))
            PrintException()
            #__save_to_parameter_data(real_estate, item, str(0), is_send_email=True)
    
    for item in transport_dist:
        try:
            count = __get_near_places(apiKey = keyAPI, lat = lat, lng = lng, place = item.name_ru, distance = 1.00)
                        
            result[item.name] = count
            __save_to_parameter_data(real_estate, item, str(count) + ' dist', is_send_email=True)
        except Exception as e:
            if is_send_email:
                send_error(str(e))
            PrintException()
            #__save_to_parserparameter_data(real_estate, item, str(0), is_send_email=True)

    return result
