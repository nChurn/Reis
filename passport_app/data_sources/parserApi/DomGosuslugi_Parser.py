import json
import requests

from passport_app.data_sources.parserApi.BaseParserApi import *

class DomGosuslugi_Parser(BaseParserApi):
    def __init__(self, subject, district, city, locality, street, numberTown):
        super.__init__(subject, district, city, locality, street, numberTown)
        self.url = 'gos'
        
        self.subject = subject
        self.district = district
        self.city = city
        self.locality = locality
        self.street = street
        self.numberTown = numberTown

    def get_request_data(self):
        return {
            'success': True,
            'result': {
                'subject': self.subject,
                'district': self.district,
                'city': self.city,
                'locality': self.locality
                'street': self.street
                'numberTown': self.numberTown
            }
        }

    def get_dict_from_resp(self, resp_text):
        json = json.loads(resp)
        return json['result']['info']#TODO alll