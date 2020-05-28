import logging

import googlemaps
from googleplaces import GooglePlaces, lang, ranking

from passport_app.email_manager import send_error
from passport_app.models import *
from passport_app.print_exception import *

logger = logging.getLogger(__name__)

class GoogleMapsAPI:
    # __real_estate : RealEstate
    # api_key = ''
    # is_send_email = False


    def __init__(self, real_estate: RealEstate, api_key, is_send_email):
        self.__real_estate = real_estate
        self.api_key = api_key
        self.is_send_email = is_send_email

        logger.info("INIT google maps api")    
        self.google_places = GooglePlaces(self.api_key)
        self.gmaps = googlemaps.Client(key=self.api_key)



    def parse_info(self, lang_code):   
        result = {}
        print("START google maps api")
                          
        lang = self.__get_lang(lang_code)
        print("get lang: %s" % (lang))

        address_convert = self.gmaps.geocode(self.__real_estate.address)
        address_coord = address_convert[0]['geometry']['location']
        print('search point: ' + str(address_coord))

        social_infr = ParserParameter.objects.filter(parser_parameter_type='social', parser_type_id = 2)#TODO change id to object
        transport_dist = ParserParameter.objects.filter(parser_parameter_type='transport_dist', parser_type_id = 2)

        for social_param in social_infr:
            try:                
                param_lang_name = self.__get_parameter_name_by_lang(lang_code, social_param)
                count = self.__get_places(address_coord, param_lang_name, lang)
                
                result[social_param.name] = count
                self.__save_to_parameter_data(social_param, str(count))
            except Exception as e:
                if is_send_email:
                    send_error(str(e))
                PrintException()
            
        for dist_param in transport_dist:
            try:
                item_lang_name = self.__get_parameter_name_by_lang(lang_code, dist_param)
                dist = self.__get_distanse(address_coord, item_lang_name, lang)   

                self.__save_to_parameter_data(dist_param, str(dist))
            except Exception as e:
                if self.is_send_email:
                    send_error(str(e))
                PrintException()
                
        return result

    def __get_lang(self, lang_code):
        if lang_code == "ru":
            return lang.RUSSIAN
        return lang.ENGLISH

    def __get_parameter_name_by_lang(self, lang_code, param):
        if lang_code == "ru":
            return param.name_ru
        
        return param.name

    def __get_places(self, address_coord, term, lang, is_send_email = False):
        try:
            term = term.replace('Google', '')

            print('place ' + term + " " + str(address_coord))
            query_result = self.google_places.nearby_search(lat_lng=address_coord,
                language=lang, keyword=term, radius=1000)

            return len(query_result.places)#TODO check
        except Exception as e:
            if is_send_email:
                send_error(str(e))
            PrintException()
            
        return 0

    def __get_distanse(self, address_coord, placename, lang):
        try:
            print('dist ' + placename + " " + str(address_coord))
            result_tr = self.google_places.nearby_search(location=self.__real_estate.address, language=lang, keyword=placename, radius=1000, rankby=ranking.DISTANCE)
            
            if len(result_tr.places) > 0:
                near_place = result_tr.places[0].geo_location
                distwalk = self.gmaps.distance_matrix(address_coord, near_place, mode='walking')
                distance = distwalk['rows'][0]['elements'][0]['distance']['value']
                return distance
            
            return ""
        except Exception as e:
            if self.is_send_email:
                send_error(str(e))
            PrintException()
            
        return 0

    def __save_to_parameter_data(self, parser_parameter, value):
        parser_parameter = ParserParameter.objects.get(name = parser_parameter.name)
        
        try:
            parameter = Parameter.objects.get(name_ru = parser_parameter.name_ru.replace('Google', '').strip())
            parameter_data = ParameterData()

            parameter_data.value = value
            parameter_data.real_estate = self.__real_estate
            parameter_data.parameter = parameter
            parameter_data.comment = 'google'
            parameter_data.save()
        except Exception as e:
            logger.error('Parameter not found in db:' + parser_parameter.name)
            if self.is_send_email:
                send_error(str(e))
                PrintException()
