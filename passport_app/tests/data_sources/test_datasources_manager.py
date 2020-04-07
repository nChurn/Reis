
from django.test import RequestFactory, TestCase
from passport_app.data_sources import search_by_jkh

class DataSourcesManagerTest(TestCase):

    def test_search_data(self):
        result = search_by_jkh("", [])
        self.assertEqual(result, {})
