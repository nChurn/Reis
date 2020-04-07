from passport_app.models import *
from django.test import RequestFactory, TestCase
from passport_app.data_sources.parser.reforma_gkh import search
from passport_app.api.ru.yandexmaps_api import yandex_get_address_data

class ReformaGkhParserTest(TestCase):

    def test_search(self):
        owner = Owner()
        owner.save()

        user = User()
        user.save()

        real_estate = RealEstate()
        real_estate.owner = owner
        real_estate.user = user
        base_address = yandex_get_address_data("г. Москва, кв-л. Юго-Запада 38-й, к. 1") 
        print(base_address)
        real_estate.country_name = base_address['country']
        real_estate.region_name = base_address['province']
        real_estate.district_name = base_address['province2']
        real_estate.locality_name = base_address['locality']
        real_estate.street_name = base_address['street']
        real_estate.house_number = base_address['house']
        real_estate.address = base_address['text_address']
        real_estate.save()
        
        parser_type = ParserType()
        parser_type.name = 'reformagkh.ru'
        parser_type.save()

        parameter_parser_1 = ParserParameter()
        parameter_parser_1.name = 'gutter_system_type'
        parameter_parser_1.name_ru = 'Тип системы водостоков'
        parameter_parser_1.parser_type = parser_type
        parameter_parser_1.parser_parameter_type = ''
        parameter_parser_1.save()


        result = search("г. Москва, кв-л. Юго-Запада 38-й, к. 1", real_estate)
        self.assertEqual(result['additional_information_about_the_property'], 'Не заполнено')
        self.assertEqual(result['total_area_common_premises'], '30 011,50')
        self.assertEqual(result['type_of_foundation'], 'Ленточный')
        self.assertEqual(result['number_of_garbage_chutes'], '5')
        self.assertEqual(result['type_of_power_supply_system'], 'Центральное')
        res_count = ParserParameterData.objects.all().count()
        self.assertEqual(res_count, 1)
        parser_parameter_data = ParserParameterData.objects.filter(parser_parameter = parameter_parser_1).first()
        self.assertEqual(parser_parameter_data.value, 'Внутренние водостоки')



        