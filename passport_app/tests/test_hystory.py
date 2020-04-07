
from django.test import RequestFactory, TestCase
from passport_app.models import *
from passport_app.api.ru.yandexmaps_api import yandex_get_address_data

class HystoryTest(TestCase):

    def test_hystory_search(self):
        base_address = {
            'country': 'Россия', 
            'province2':'Московская область', 
            'locality':'Электросталь', 
            'province':'Центральный федеральный округ',
            'street':'проспект Ленина',
            'house':'1',
            'text_address':'Россия, Московская область, Электросталь, проспект Ленина, 1'
            }

        print(base_address)

        owner = Owner()
        owner.save()

        user = User()
        user.save()

        real_estate1 = RealEstate()
        real_estate1.owner = owner
        real_estate1.user = user
        
        real_estate1.country_name = base_address['country']
        real_estate1.region_name = base_address['province']
        real_estate1.district_name = base_address['province2']
        real_estate1.locality_name = base_address['locality']
        real_estate1.street_name = base_address['street']
        real_estate1.house_number = base_address['house']
        real_estate1.address = base_address['text_address']
        real_estate1.save()

        real_estate2 = RealEstate()
        real_estate2.owner = owner
        real_estate2.user = user
        real_estate2.country_name = base_address['country']
        real_estate2.region_name = base_address['province']
        real_estate2.district_name = base_address['province2']
        real_estate2.locality_name = base_address['locality']
        real_estate2.street_name = base_address['street']
        real_estate2.house_number = base_address['house']
        real_estate2.address = base_address['text_address']
        real_estate2.save()

        base_address1 = {
            'country': 'Россия', 
            'province2':'Москва', 
            'locality':'Электросталь', 
            'province':'Центральный федеральный округ',
            'street':'Новочеркасский бульвар',
            'house':'51',
            'text_address':'Россия, Москва, Новочеркасский бульвар, 51'
            }
        print(base_address1)

        real_estate3 = RealEstate()
        real_estate3.owner = owner
        real_estate3.user = user
        real_estate3.country_name = base_address1['country']
        real_estate3.region_name = base_address1['province']
        real_estate3.district_name = base_address1['province2']
        real_estate3.locality_name = base_address1['locality']
        real_estate3.street_name = base_address1['street']
        real_estate3.house_number = base_address1['house']
        real_estate3.address = base_address1['text_address']
        real_estate3.save()

        result = RealEstate.objects.filter(user = user, address = real_estate1.address).count()
        result2 = RealEstate.objects.filter(user = user, address = real_estate3.address).count()
        self.assertEqual(result, 2)
        self.assertEqual(result2, 1)
        result3 = RealEstate.objects.filter(user = user, address = real_estate1.address)
        self.assertEqual(result3[0].address, 'Россия, Московская область, Электросталь, проспект Ленина, 1')

