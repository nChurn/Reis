from abc import ABC, abstractmethod
import requests
import json

class BaseApiParser(ABC):
    def __init__(self, domain, url):
        self.domain = domain
        self.url = url

    def start(self):
        post_data = self.get_request_data()
        resp = requests.post(self.domain + '/' + self.url, json.dumps(post_data))

        return self.get_dict_from_resp(resp)

    @abstractmethod
    def get_request_data(self):
        pass

    @abstractmethod
    def get_dict_from_resp(self, resp):
        pass