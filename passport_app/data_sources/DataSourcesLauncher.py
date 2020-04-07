from passport_app.models import *
from passport_app.data_sources.api.GoogleMapsAPI import GoogleMapsAPI
import logging

class DataSourcesLauncher():
    __real_estate : RealEstate

    def __init__(self, real_estate: RealEstate):
        self.__real_estate = real_estate

    def start_parsing(self):
        logger = logging.getLogger(__name__)
        result = {}
        
        parsers = ParserType.objects.order_by('id').all()
        for parser in parsers:
            if parser.name == 'google_map':
                p = GoogleMapsAPI(self.__real_estate, parser.authkey, False)
                google_result = p.parse_info('ru')

                self.__save_data(google_result)

            # if parser.name == 'yandex_map':
            #     social = ParserParameter.objects.filter(parser_parameter_type='social', parser_type = None)
            #     dist = ParserParameter.objects.filter(parser_parameter_type='transport_dist', parser_type = None)
                
            #     yandex_result = yandex_search(keyAPI =  parser.authkey, address = address,
            #         social_infr = social, transport_dist = dist, real_estate = real_estate, 
            #         lang_code = 'ru', is_send_email = False)

            #     self.__save_data(yandex_result)


    def __save_data(self, data):
        pass
    