
from django.test import RequestFactory, TestCase
from passport_app.data_sources.api.yandexmaps import yandex_search
from passport_app.models import *
import logging

class YandexMapsTest(TestCase):

    def test_search(self):
        logger = logging.getLogger(__name__)
        KEY = 'AIzaSyCyqz9VIBoX2nEiKkFqu2MiQKkqevR7K6w'
        owner = Owner()
        owner.save()

        user = User()
        user.save()

        real_estate = RealEstate()
        real_estate.owner = owner
        real_estate.user = user
        real_estate.save()
        # print(search('Москва, Волжский Бульвар 113 А, к. 2'))
        # print(search('Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31'))
        # keyAPI, address, social_infr, transport_dist, lang_code, is_send_email = False
        parser_type = ParserType()
        parser_type.name = 'yandex_map'
        parser_type.save()

        parameter_parser_1 = ParserParameter()
        parameter_parser_1.name = 'test1'
        parameter_parser_1.name_ru = 'Высшее учебное заведение ВУЗ'
        parameter_parser_1.parser_type = parser_type
        parameter_parser_1.parser_parameter_type = 'social'
        parameter_parser_1.save()

        parameter_parser_2 = ParserParameter()
        parameter_parser_2.name = 'test2'
        parameter_parser_2.name_ru = 'Станция метро'
        parameter_parser_2.parser_type = parser_type
        parameter_parser_2.parser_parameter_type = 'transport_dist'
        parameter_parser_2.save()

        social_infr = ParserParameter.objects.filter(parser_type = parser_type, 
                                                    parser_parameter_type = 'social').all()
        dist = ParserParameter.objects.filter(parser_type = parser_type, 
                                                    parser_parameter_type = 'transport_dist').all()
        logger.error("distance")
        logger.error(dist)
        logger.error("social")
        logger.error(social_infr)
        yandex_search(keyAPI = KEY, address = 'Г. МОСКВА, УЛ. ЛЕТЧИКА БАБУШКИНА, Д. 31',
        social_infr = social_infr, transport_dist = dist, real_estate = real_estate, lang_code = 'ru', is_send_email = False)
        logger.error("parameter data")
        logger.error(ParserParameterData.objects.all())
        res_count = ParserParameterData.objects.all().count()
        self.assertEqual(res_count, 2)
