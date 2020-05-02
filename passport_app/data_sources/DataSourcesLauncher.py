import logging
from django.db.models import Q

from passport_app.data_sources.api.GoogleMapsAPI import GoogleMapsAPI
from passport_app.data_sources.api.YandexMapsAPI import YandexMapsAPI
from passport_app.data_sources.parser.ReformaGkh_Parser import ReformaGkh_Parser
from passport_app.models import *
from passport_app.data_sources.parser.pkk_rosreestr.Pkk_Rosreestr_Parser import Pkk_Rosreestr_Parser

logger = logging.getLogger(__name__)

class DataSourcesLauncher():
    __real_estate : RealEstate

    def __init__(self, real_estate: RealEstate):
        self.__real_estate = real_estate

    def start_parsing(self):              
        result = {}
        
        parsers = ParserType.objects.order_by('id').all()
        for parser in parsers:
            # if parser.name == 'google_map':
            #     p = GoogleMapsAPI(self.__real_estate, parser.authkey, False)
            #     google_result = p.parse_info('ru')

            #     #self.__save_data(google_result)

            # if parser.name == 'yandex_map':
            #     p = YandexMapsAPI(self.__real_estate, parser.authkey, 'c687c609-ae0e-4b12-8d9a-aab953d8642f', False)
            #     yandex_result = p.parse_info('ru')

                #self.__save_data(yandex_result)

            if parser.name == 'rosreestr.ru':            
                p = Pkk_Rosreestr_Parser()
                data = p.parse_data(self.__real_estate)

                self.__save_data(data)

            if parser.name == 'reformagkh.ru':
                p = ReformaGkh_Parser()
                p.parse_data(self.__real_estate.address, self.__real_estate)


    def __save_data(self, data):
        for item_key in data:
            try:
                parser_parameter = ParserParameter.objects.get(name = item_key)
            except Exception as e:
                logger.error('Parser parameter not found in db: ' + item_key)
                logger.error('')
                logger.error('')
                continue

            try:
                parameter = Parameter.objects.get(name_ru = parser_parameter.name_ru)
                parameter_data = ParameterData()

                parameter_data.value = '' if data[item_key] is None else data[item_key]
                parameter_data.real_estate = self.__real_estate
                parameter_data.parameter = parameter
                parameter_data.save()
            except Exception as e:
                logger.error('Parameter not found in db: ' + item_key + " " + parser_parameter.name_ru)
                logger.error(str(e))
                logger.error('')
                logger.error('')
