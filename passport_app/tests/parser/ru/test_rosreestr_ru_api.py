from django.test import TestCase
from passport_app.parser.ru.rosreestr_ru_api import selenium_rosreestr
from operator import itemgetter

class ApiTestCase(TestCase):

    def test_selenium_rosreestr(self):
        # search('Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31')
        address = 'Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31'
        kadastr_number = ''
        result = selenium_rosreestr(kadastr_number)
        print (result)
        self.assertEqual(result, 'accuracy_of_land_boundaries')