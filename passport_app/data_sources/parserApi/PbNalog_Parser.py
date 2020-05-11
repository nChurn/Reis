import json
import requests

from passport_app.data_sources.parserApi.BaseParserApi import *

class PbNalog_Parser(BaseParserApi):
    def __init__(self, fio, inn, ogrn, name):
        print("start PbNalog")
        super().__init__(fio, inn, ogrn, name)
        self.url = 'getNalog'

    def get_request_data(self):
        return self.get_request_data_default()

    def get_dict_from_resp(self, json_obj):
        data = json_obj['result']['info']
        result = {}

        result['multi_boss'] = data['3']
        result['multi_creators'] = data['4']
        result['in_reestr'] = data['5']
        result['multi_address'] = data['6']
        result['info_129_fz'] = data['8']

        return result
