import json
import requests

from passport_app.data_sources.parserApi.BaseParserApi import *


class Fcin_Parser(BaseParserApi):
    def __init__(self, fio, inn, ogrn, name):
        super().__init__(fio, inn, ogrn, name)
        self.url = 'getCrime'

    def get_request_data(self):
        return self.get_request_data_default()

    def get_dict_from_resp(self, json_obj):
        data = json_obj['result']['info']

        result = {}
        result['person_wanted'] = "Да" if data != 'Информация не найдена' else 'Нет'

        return result
