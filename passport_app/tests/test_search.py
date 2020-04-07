from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from passport_app.views import *

class SearchTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='admin', email='jacob@…', password='admin')

    # def test_update_details(self):
    #     # Create an instance of a GET request.
    #     request = self.factory.get('/search/')
    #     response = SearchView.as_view()(request)
    #     request.kadastr_number = "77:02:0011006:1501"
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_update_details(self):
    #     # Create an instance of a GET request.
    #     request = self.factory.get('/search/')
    #     response = SearchView.as_view()(request)
    #     request.kadastr_number = "60:27:0050402:173"
    #     self.assertEqual(response.status_code, 200)

    # def test_update_details(self):
    #     # Create an instance of a GET request.
    #     request = self.factory.get('/search/')
    #     response = SearchView.as_view()(request)
    #     request.kadastr_number = "32:28:0020314:13"
    #     self.assertEqual(response.status_code, 200)