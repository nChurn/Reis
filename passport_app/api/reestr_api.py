from urllib.parse import urlencode
import requests
import json
from passport_app.api.ru.rosreestr_5kk import rosreestr_details_5kk
from passport_app.api.ru.googlemaps_api import google_search
from passport_app.parser.ru.rosreestr_net_parser import search_by_cn

REQ_TIMEOUT = 10


def _get_data_from_pkk(kadastr_number, contains):
    json_content = {}
    address = ''
    params = {
        'text': kadastr_number,
        'tolerance': '1',  # приближение карты
        'limit': '11'  # лимит ответов, мы берем всегда первый
    }

    url_params = urlencode(params)
    type = 1

    try:
        url_sttr = 'https://pkk5.rosreestr.ru/api/features/' + str(
            type) + '?' + url_params
        response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
        data = response.text
        json_content = json.loads(data)
    except (KeyError, TypeError, IndexError, requests.Timeout):
        pass

    print('_get_data_from_pkk first request')
    if json_content and len(json_content['features']) == 0:
        type = 5
        try:
            url_sttr = 'https://pkk5.rosreestr.ru/api/features/' + str(
                type) + '?' + url_params
            response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
            if response.status_code == 200:
                data = response.text
                json_content = json.loads(data)
        except (KeyError, TypeError, IndexError, requests.Timeout):
            pass

    try:  # кадастровый номер здания
        cn = json_content['features'][0]['attrs']['cn']
        contains['base']['kadastr_number'] = cn
    except (KeyError, TypeError, IndexError):
        pass

    try:  # местоположение
        address = json_content['features'][0]['attrs']['address']
        contains['base']['address'] = address
        print(address)
    except (KeyError, TypeError, IndexError):
        pass

    # второй запрос, когда мы кликаем на найденный адресс
    print('_get_data_from_pkk second request')
    try:
        search_number = json_content['features'][0]['attrs'][
            'id']  # типо кадастрового номера только без 0
        url_sttr = 'https://pkk5.rosreestr.ru/api/features/' + str(
            type
        ) + '/' + search_number  # используем не кадастровый, а search number
        response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
        if response.status_code == 200:
            data = response.text
            json_content = json.loads(data)
            rosreestr_details_5kk(
                json_content,
                contains['place_info'])  # записываем контет в массивы
    except (KeyError, TypeError, IndexError,
            requests.Timeout):  # когда переход на адресс не удался
        pass


def _get_data_from_pkk_by_address(address, contains):
    json_content = None
    params = {
        'text': address,
        'tolerance': '1',  # приближение карты
        'limit': '11'  # лимит ответов, мы берем всегда первый
    }

    url_params = urlencode(params)
    type = 1

    url_sttr = 'https://pkk5.rosreestr.ru/api/features/' + str(
        type) + '?' + url_params
    print(url_sttr)
    try:
        response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
        data = response.text
        json_content = json.loads(data)
    except requests.Timeout:
        pass

    if not json_content or len(json_content['features']) == 0:
        type = 5
        url_sttr = 'https://pkk5.rosreestr.ru/api/features/' + str(
            type) + '?' + url_params
        print(url_sttr)
        try:
            response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
            data = response.text
            json_content = json.loads(data)
        except requests.Timeout:
            pass

    try:  # кадастровый номер здания
        cn = json_content['features'][0]['attrs']['cn']
        contains['base']['kadastr_number'] = cn
    except (KeyError, TypeError, IndexError):
        pass

    try:  # местоположение
        address_param = json_content['features'][0]['attrs']['address']
        contains['base']['address'] = address
        print(address)
    except (KeyError, TypeError, IndexError):
        pass

    # второй запрос, когда мы кликаем на найденный адресс
    try:
        search_number = json_content['features'][0]['attrs'][
            'id']  # типо кадастрового номера только без 0
        url_sttr = 'https://pkk5.rosreestr.ru/api/features/' + str(
            type
        ) + '/' + search_number  # используем не кадастровый, а search number
        response = requests.get(url_sttr, timeout=REQ_TIMEOUT)
        data = response.text
        json_content = json.loads(data)

        rosreestr_details_5kk(json_content, results)  # записываем контет в массивы
    except (KeyError, TypeError, IndexError, requests.Timeout):  # когда переход на адресс не удался
        pass


def get_data_from_rosreesr_api_by_cn(cn, params):
    #kadastr_number = "77:03:0003019:72"
    search_by_cn(cn, params)
    address = params['base']['address']
    # _get_data_from_pkk(cn, params)
    # google_search(address, params)


def get_data_from_rosreesr_api_by_address(address, params):
    kadastr_number = "77:03:0003019:72"

    # _get_data_from_pkk_by_address(address, params)
    # google_search(address, params)
