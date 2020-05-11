import json
import requests

from passport_app.data_sources.parserApi.BaseParserApi import *
from passport_app.models import *

class DomGosuslugi_Parser(BaseParserApi):
    def __init__(self, subject, district, city, locality, street, numberTown):
        print("start DomGosuslugi")
        super().__init__(None, None, None, None)
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
                'locality': self.locality,
                'street': self.street,
                'numberTown': self.numberTown
            }
        }

    def get_dict_from_resp(self, json_obj):
        data = json['result']['info']
        parser_params = ParserParameter.objects.filter(parser_type_id = self.parser_type.id)

        keys = data.keys()
        result = {}
        for parser_param in parser_params:
            matches = [x for x in keys if parser_param.name_ru in x]
            if len(match) > 0:
                result[parser_param.name_ru] = data[match]

        return result


