from django.test import TestCase
from passport_app.api.reestr_api import get_data_from_rosreesr_api_by_address, get_data_from_rosreesr_api_by_cn
from operator import itemgetter

class ApiTestCase(TestCase):

    def test_api(self):
        # search('Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31')
        params = {'social': {}, 'transport': {}, 'place_info': {}, 'rights': {}, 'architecture': {}, 'engsys': {},
                  'base': {}}
        get_data_from_rosreesr_api_by_cn('77:03:0003019:72', params)
        get_data_from_rosreesr_api_by_address('Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31', params)
        self.assertEqual(result['accuracy_of_land_boundaries'], {'ymin': 7532857.897858755, 'xmax': 4193955.992591603,
                                                                 'ymax': 7532868.432771631, 'xmin': 4193937.428292963})