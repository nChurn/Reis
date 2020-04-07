from passport_app.models import *
from passport_app.data_sources.api.googlemaps import google_search
from passport_app.data_sources.api.yandexmaps import yandex_search
from passport_app.data_sources.api.reformagkh import search_by_jkh
from passport_app.email_manager import send_error
import logging

from passport_app.data_sources.parser.ReformaGkh_Parser import ReformaGkh_Parser
from passport_app.data_sources.parser.pkk_rosreestr.Pkk_Rosreestr_Parser import *

logger = logging.getLogger(__name__)

def __save_parser_data(parser_parameter, real_estate, value, is_send_email = False):
    try:
        parser_parameter_data = ParserParameterData()
        parser_parameter_data.value = value
        parser_parameter_data.real_estate = real_estate
        parser_parameter_data.parser_parameter = parser_parameter
        parser_parameter_data.save()
    except Exception as e:
        if is_send_email:
            send_error(str(e))
        logger.error(str(e))
        pass

def __test_empty_data(parser_parameters, real_estate):
    for item in parser_parameters:
        __save_parser_data(parser_parameter = item, real_estate = real_estate, value = "") 

def __save_info_to_db(result, real_estate):
    for item_key in result:
        try:
            parser_parameter = ParserParameter.objects.get(name = item_key)

            parameter = Parameter.objects.get(name_ru = parser_parameter.name_ru)
            parameter_data = ParameterData()

            parameter_data.value = result[item_key]
            parameter_data.real_estate = real_estate
            parameter_data.parameter = parameter
            parameter_data.save()
        except Exception as e:
            logger.error('Parser parameter not found in db:' + item_key)
            logger.error(str(e))

def start_search_info(address, real_estate):
    parsers = ParserType.objects.order_by('id').all()
    result = {}
    for parser in parsers:
        # if parser.name == 'google_map':
        #     social = ParserParameter.objects.filter(parser_parameter_type='social', parser_type = None)
        #     dist = ParserParameter.objects.filter(parser_parameter_type='transport_dist', parser_type = None)

        #     google_result = google_search(keyAPI = parser.authkey, address = address,
        #         social_infr = social, transport_dist = dist,
        #         real_estate = real_estate, lang_code = 'ru', is_send_email = False)

        #     #__save_info_to_db(google_result, real_estate)
            
        if parser.name == 'yandex_map':
            print ('yandex_map')
            print(parser.name)

            social = ParserParameter.objects.filter(parser_parameter_type='social', parser_type = None)
            dist = ParserParameter.objects.filter(parser_parameter_type='transport_dist', parser_type = None)
            
            yandex_result = yandex_search(keyAPI =  parser.authkey, address = address,
                social_infr = social, transport_dist = dist, real_estate = real_estate, 
                lang_code = 'ru', is_send_email = False)

            #__save_info_to_db(yandex_result, real_estate)

            
        
        # if parser.name == 'yandex_transport':
        #     print ('yandex_transport')
        #     parser_parameters = ParserParameter.objects.filter(parser_type=parser)
        #     __test_empty_data(parser_parameters = parser_parameters, real_estate = real_estate)
        # if parser.name == 'wiki_routes':
        #     print ('wiki_routes')
        #     parser_parameters = ParserParameter.objects.filter(parser_type=parser)
        #     __test_empty_data(parser_parameters = parser_parameters, real_estate = real_estate)

        if parser.name == 'rosreestr.ru':            
            # parser_parameters = ParserParameter.objects.filter(parser_type=parser)
            # __test_empty_data(parser_parameters = parser_parameters, real_estate = real_estate)

            p = Pkk_Rosreestr_Parser()
            data = p.parse_data(address, real_estate)

            __save_info_to_db(data, real_estate)

        if parser.name == 'reformagkh.ru':
            p = ReformaGkh_Parser()
            p.parse_data(address, real_estate)

