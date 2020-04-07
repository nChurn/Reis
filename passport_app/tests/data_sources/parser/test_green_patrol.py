
from django.test import RequestFactory, TestCase
from passport_app.data_sources.parser.green_patrol import search

class GreenPatrolTest(TestCase):

    def test_search(self):
        result = search("Смоленская")
        self.assertEqual(result, {})
