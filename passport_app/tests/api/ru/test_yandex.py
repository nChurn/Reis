from django.test import TestCase

from passport_app.api.ru.yandexmaps_api import *


class YandexTestCase(TestCase):

    def test_yandex_get_address_data(self):
        params = {
                "country": "Россия",
                "house": "24",
                "locality": "Москва",
                "province": "Центральный федеральный округ",
                "province2": "Москва",
                "street": "улица Новый Арбат",
                "text_address": "Россия, Москва, улица Новый Арбат, 24",
                "point": "37.587614 55.753083"
                }

        # print(search('Москва, Волжский Бульвар 113 А, к. 2'))
        # print(search('Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31'))
        result = yandex_get_address_data('Москва, улица Новый Арбат, дом 24')
        self.assertEqual(result['country'], params['country'])
        self.assertEqual(result['house'], params['house'])
        self.assertEqual(result['locality'], params['locality'])
        self.assertEqual(result['province'], params['province'])
        self.assertEqual(result['province2'], params['province2'])
        self.assertEqual(result['street'], params['street'])
        self.assertEqual(result['text_address'], params['text_address'])
        self.assertEqual(result['point'], params['point'])
