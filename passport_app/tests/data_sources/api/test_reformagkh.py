
from django.test import RequestFactory, TestCase
from passport_app.data_sources.api.reformagkh import search_by_jkh

class ReformagkhTest(TestCase):

    def test_search(self):
        result = search_by_jkh("", [])
        self.assertEqual(result, {})
