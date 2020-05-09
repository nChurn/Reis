import json
import requests

class BankrotFedres_Parser():
    def __init__(self, fio, inn, ogrn, name):
        self.domain = 'http://81.177.175.19:8080'
        self.url = 'getBankrot'

        self.fio = fio
        self.inn = inn
        self.ogrn = ogrn
        self.name = name

    def __get_request_data(self):
        return {
            'success': True,
            'result': {
                'fio': self.fio,
                'inn': self.inn,
                'ogrn': self.ogrn,
                'name': self.name
            }
        }

    def __get_dict_from_resp(self, json_obj):
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

    def get_result(self):
        post_data = self.__get_request_data()
        resp = requests.post(self.domain + '/' + self.url, json=post_data)

        return self.__get_dict_from_resp(resp.json())