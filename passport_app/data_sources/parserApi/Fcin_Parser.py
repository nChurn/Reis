import json
import requests

class Fcin_Parser():
    def __init__(self, fio, inn, ogrn, name):
        self.domain = 'http://81.177.175.19:8080'
        self.url = 'getCrime'

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
        result['person_wanted'] = "Да" if data != 'Информация не найдена' else 'Нет'

        return result

    def getResult(self):
        post_data = self.get_request_data()
        resp = requests.post(self.domain + '/' + self.url, json=post_data)

        return self.get_dict_from_resp(resp.json())