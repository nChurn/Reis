from django.test import RequestFactory, TestCase
from passport_app.parser.ru.reforma_gkh_parser import search

class ApiTestCase(TestCase):

    def test_gkh(self):
        result = {}
        search( "г.Москва, пл.Славянская, д.4, стр.1", result)
        print (result)
        self.assertEqual("", result)