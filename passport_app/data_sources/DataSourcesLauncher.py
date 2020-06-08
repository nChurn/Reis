import logging
from django.db.models import Q
from django.db import connection

from passport_app.data_sources.api.GoogleMapsAPI import GoogleMapsAPI
from passport_app.data_sources.api.YandexMapsAPI import YandexMapsAPI
from passport_app.data_sources.parser.ReformaGkh_Parser import ReformaGkh_Parser
from passport_app.models import *
from passport_app.data_sources.parser.pkk_rosreestr.Pkk_Rosreestr_Parser import Pkk_Rosreestr_Parser
from passport_app.data_sources.parser.Avito_Parser import Avito_Parser
from passport_app.data_sources.parser.Cian_Parser import Cian_Parser
from passport_app.data_sources.parserApi.BankrotFedres_Parser import BankrotFedres_Parser
from passport_app.data_sources.parserApi.PbNalog_Parser import PbNalog_Parser
from passport_app.data_sources.parserApi.Fcin_Parser import Fcin_Parser
from passport_app.data_sources.parserApi.KadArbitr_Parser import KadArbitr_Parser
from passport_app.data_sources.parserApi.DomGosuslugi_Parser import DomGosuslugi_Parser


logger = logging.getLogger(__name__)

class DataSourcesLauncher():
    # __real_estate : RealEstate

    def __init__(self, real_estate: RealEstate):
        self.__real_estate = real_estate

    def start_parsing(self):              
        parsers = ParserType.objects.order_by('id').all()
        for parser in parsers:
            # if parser.name == 'google_map':
            #     p = GoogleMapsAPI(self.__real_estate, parser.authkey, False)
            #     google_result = p.parse_info('ru')

            #     #self.__save_data(google_result)

            # if parser.name == 'yandex_map':
            #     p = YandexMapsAPI(self.__real_estate, parser.authkey, 'c687c609-ae0e-4b12-8d9a-aab953d8642f', False)
            #     yandex_result = p.parse_info('ru')

            #     self.__save_data(yandex_result)

            # if parser.name == 'rosreestr.ru':            
            #     p = Pkk_Rosreestr_Parser()
            #     data = p.parse_data(self.__real_estate)
            #     self.__save_data(data)

            # if parser.name == 'reformagkh.ru':
            #     p = ReformaGkh_Parser()
            #     p.parse_data(self.__real_estate.address, self.__real_estate)

            # if self.__real_estate.owner.name or self.__real_estate.owner.inn:
            #     # if parser.url == 'http://bankrot.fedresurs.ru/':
            #     #     p = BankrotFedres_Parser(self.__real_estate.owner.name, self.__real_estate.owner.inn, None, self.__real_estate.owner.name)
            #     #     self.__save_data(p.get_result())

            #     if parser.url == 'https://pb.nalog.ru/':
            #         p = PbNalog_Parser(self.__real_estate.owner.name, self.__real_estate.owner.inn, None, self.__real_estate.owner.name)
            #         self.__save_data(p.get_result())

            #     if parser.url == 'https://kad.arbitr.ru/':
            #         p = KadArbitr_Parser(self.__real_estate.owner.name, self.__real_estate.owner.inn, None, self.__real_estate.owner.name)
            #         self.__save_data(p.get_result())
                    
            #     if parser.url == 'http://xn--h1akkl.xn--p1ai/':#фсин
            #         p = Fcin_Parser(self.__real_estate.owner.name, self.__real_estate.owner.inn, None, None)
            #         self.__save_data(p.get_result())
            
            # if parser.url == 'https://dom.gosuslugi.ru/':
            #     p = DomGosuslugi_Parser(self.__real_estate.region_name, self.__real_estate.district, 
            #         self.__real_estate.locality, None, 
            #         self.__real_estate.street_name, self.__real_estate.house_number)
            #     p.parser_type = parser

            #     self.__save_data(p.get_result())

            if parser.url == "https://www.avito.ru/":
                p = Avito_Parser()
                self.__save_data(p.pase_data(self.__real_estate.address))

            # if parser.url == "https://cian.ru/":
            #     p = Cian_Parser()
            #     self.__save_data(p.pase_data(self.__real_estate.address))


    def __save_data(self, data):
        for item_key in data:
            try:
                parser_parameter = ParserParameter.objects.get(name = item_key)
            except Exception as e:
                logger.error('Parser parameter not found in db: ' + item_key)
                continue

            try:
                cursor = connection.cursor()
                cursor.execute('''SELECT * FROM public.passport_app_parameter_parser_parameters
                    where parserparameter_id = ''' + str(parser_parameter.id)) 

                rows = cursor.fetchall()
                for row in rows:
                    param = Parameter.objects.get(pk= row[1])

                    parameter_data = ParameterData()
                    parameter_data.value = '' if data[item_key] is None else data[item_key]
                    parameter_data.real_estate = self.__real_estate
                    parameter_data.parameter = param
                    parameter_data.save()
            except Exception as e:
                logger.exception('fail to save item key: ' + item_key, e)
