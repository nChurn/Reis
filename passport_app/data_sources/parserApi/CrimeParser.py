import json
import requests

class ArbParser():
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

    def get_dict_from_resp(self, resp_text):
        json = json.loads(resp)
        return json['result']['info']

    def getResult(self):
        post_data = self.get_request_data()
        resp = requests.post(self.domain + '/' + self.url, json.dumps(post_data))

        return self.get_dict_from_resp(resp.text)