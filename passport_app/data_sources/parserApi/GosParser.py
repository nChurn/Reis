import json
import requests

class ArbParser():
    def __init__(self, subject, district, city, locality, street, numberTown):
        self.domain = 'http://81.177.175.19:8080'
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
        return json['result']['info']

    def getResult(self):
        post_data = self.get_request_data()
        resp = requests.post(self.domain + '/' + self.url, json.dumps(post_data))

        return self.get_dict_from_resp(resp.text)