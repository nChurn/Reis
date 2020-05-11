import json
import requests

from passport_app.data_sources.parserApi.BaseParserApi import *

class KadArbitr_Parser(BaseParserApi):
    def __init__(self, fio, inn, ogrn, name):
        print("start KadArbitr")
        super().__init__(fio, inn, ogrn, name)
        self.url = 'getArb'

        self.fio = fio
        self.inn = inn
        self.ogrn = ogrn
        self.name = name

    def get_request_data(self):
        return self.get_request_data_default()

    def get_dict_from_resp(self, json_obj):
        data = json_obj['result']['info']
        result = {}

        obj = data['kartoteka']['administrative']
        if self.__check_is_empty(obj):
            result['owner_cases_count_admin'] = 0
        else:
            result['owner_cases_count_admin'] = len(obj['date'])

        obj = data['kartoteka']['civil']
        if self.__check_is_empty(obj):
            result['owner_cases_count_civil'] = 0
        else:
            result['owner_cases_count_civil'] = len(obj['date'])

        obj = data['kartoteka']['bankruptcy']
        if self.__check_is_empty(obj):
            result['owner_cases_count_bankruptcy'] = 0
        else:
            result['owner_cases_count_bankruptcy'] = len(obj['date'])

        result['owner_cases_count_arbitr'] = ''
        result['owner_cases_count_orders'] = ''

        return result

    def __check_is_empty(self, dict):
        if dict['0'] == 'Нет результатов':
            return True
        return False        