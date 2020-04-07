
from django.test import RequestFactory, TestCase
from passport_app.email_manager import *

class EmailTest(TestCase):

    def test_send_email(self):
        result = send_search_result({}, {}, {})
        self.assertEqual(result, None)
