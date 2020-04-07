from passport_app.models import *


class DataSourcesLauncher():
    __real_estate : RealEstate

    def __init__(self, real_estate: RealEstate):
        self.__real_estate = real_estate

    def start_parsing():
        logger = logging.getLogger(__name__)
        result = {}
        
        parsers = ParserType.objects.order_by('id').all()
        for parser in parsers:
            if parser.name == 'google_map':
                social = ParserParameter.objects.filter(parser_parameter_type='social', parser_type = None)
                dist = ParserParameter.objects.filter(parser_parameter_type='transport_dist', parser_type = None)

                google_result = google_search(keyAPI = parser.authkey, address = address,
                    social_infr = social, transport_dist = dist,
                    real_estate = real_estate, lang_code = 'ru', is_send_email = False)

                self.__save_data(google_result)

            if parser.name == 'yandex_map':
                social = ParserParameter.objects.filter(parser_parameter_type='social', parser_type = None)
                dist = ParserParameter.objects.filter(parser_parameter_type='transport_dist', parser_type = None)
                
                yandex_result = yandex_search(keyAPI =  parser.authkey, address = address,
                    social_infr = social, transport_dist = dist, real_estate = real_estate, 
                    lang_code = 'ru', is_send_email = False)

                self.__save_data(yandex_result)


    def __save_data(self, data):
        pass