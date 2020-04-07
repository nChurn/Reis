from django.test import TestCase
from passport_app.parser.ru.rosreestr_net_parser import search_by_cn
from operator import itemgetter

class ApiTestCase(TestCase):

    def test_rosreestr_net_rosreestr(self):
        # search('Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31')
        params = {'social': {}, 'transport': {}, 'place_info': {}, 'rights': {}, 'architecture': {}, 'engsys': {},
                  'base': {}}
        address = 'Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31'
        kadastr_number = '76:11:050101:8'
        result = search_by_cn(kadastr_number, params)
        print (result)
        self.assertEqual(params['base']['kadastr_number'], kadastr_number)