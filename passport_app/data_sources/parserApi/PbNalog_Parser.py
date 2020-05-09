import json
import requests

class PbNalog_Parser():
    def __init__(self, fio, inn, ogrn, name):
        self.domain = 'http://81.177.175.19:8080'
        self.url = 'getNalog'

        self.fio = fio
        self.inn = inn
        self.ogrn = ogrn
        self.name = name

    def get_request_data(self):
        return {
            'success': True,
            'result': {
                'fio': self.fio,
                'inn': self.inn,
                'ogrn': self.ogrn,
                'name': self.name
            }
        }

    def get_dict_from_resp(self, json_obj):
        data = json_obj['result']['info']
        result = {}

        result['multi_boss'] = data['3']
        result['multi_creators'] = data['4']
        result['in_reestr'] = data['5']
        result['multi_address'] = data['6']
        result['info_129_fz'] = data['8']

        return result

    def getResult(self):
        post_data = self.get_request_data()
        resp = requests.post(self.domain + '/' + self.url, json=post_data)

        return self.get_dict_from_resp(resp.json())