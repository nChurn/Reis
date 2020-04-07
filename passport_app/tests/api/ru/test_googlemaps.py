from django.test import TestCase
import requests
from bs4 import BeautifulSoup
from passport_app.api.ru.googlemaps_api import google_search
from operator import itemgetter


class GooglemapsTestCase(TestCase):

    def test_ggooglemaps(self):
        params = {'social': {}, 'transport': {}, 'place_info': {}, 'rights': {}, 'architecture': {}, 'engsys': {},
                  'base': {}}
        # print(search('Москва, Волжский Бульвар 113 А, к. 2'))
        # print(search('Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31'))
        google_search('Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31', params)
        self.assertEqual(params['social']['ambulance'], 2)
