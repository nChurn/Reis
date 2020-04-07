from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from passport_app.views import *

# class DetailsUpdateTest(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             username='admin', email='jacob@…', password='admin')
#
#     def test_update_details(self):
#         # Create an instance of a GET request.
#         request = self.factory.get('/details/')