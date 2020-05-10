from abc import ABC, abstractmethod
import logging
import requests 
import json


class BaseParserApi(ABC):
    logger = logging.getLogger(__name__)

    def __init__(self, fio, inn, ogrn, name):
        self.domain = 'http://81.177.175.19:8080'
        #self.url = 'getBankrot'

        self.fio = fio
        self.inn = inn
        self.ogrn = ogrn
        self.name = name

    @abstractmethod
    def get_request_data(self):
        pass

    @abstractmethod
    def get_dict_from_resp(self, json_obj):
        pass

    def get_request_data_default(self):
        return {
            'success': True,
            'result': {
                'fio': self.fio,
                'inn': self.inn,
                'ogrn': self.ogrn,
                'name': self.name
            }
        }

    def get_result(self):
        post_data = self.get_request_data()
        try:
            resp = requests.post(self.domain + '/' + self.url, json=post_data)
        except Exception as ex:
            self.logger.exception('fail to load page: ' + self.domain + '/' + self.url, ex)
            return {}

        try:
            return self.get_dict_from_resp(resp.json())
        except Exception as ex:
            self.logger.exception('fail to parse resp for page: ' + self.domain + '/' + self.url, ex)
            return {}