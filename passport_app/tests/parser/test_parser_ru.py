from django.test import TestCase
from operator import itemgetter
from parser.parser_ru import get_data_from_rosreestr_ru
#from parser.parser_ru. import *

class ApiTestCase(TestCase):

    def test_api(self):
        # search('Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31')
        address = 'Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31'
        kadastr_number = ''
        result = get_data_from_rosreestr_ru(kadastr_number, address)
        print (result)
        result_sort = sorted(result, key=itemgetter('title'))
        self.assertEqual(result_sort[0]['title'], 'accuracy_of_land_boundaries')


p = ApiTestCase()
p.test_api()