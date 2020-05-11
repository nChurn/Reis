import json
import requests

from passport_app.data_sources.parserApi.BaseParserApi import *

class BankrotFedres_Parser(BaseParserApi):
    def __init__(self, fio, inn, orgn, name):
        print("start BankrotFedres")
        super().__init__(fio, inn, orgn, name)
        self.url = 'getBankrot'

    def get_request_data(self):
        return self.get_request_data_default()
    
    def get_dict_from_resp(self, json_obj):
        data = json_obj['result']['info']

        result = {}
        result['owner_in_bankruptcy'] = data['name']
        result['ground_owner'] = data['name']
        result['building_owner'] = data['name']
        result['room_owner'] = data['name']

        result['bankruptcy_date'] = data['date']['1']
        result['sro'] = data['sro']['1'][next(iter(data['sro']['1'].keys()))]
        result['fio_contest_manager'] = next(iter(data['sro']['1'].keys()))

        return result