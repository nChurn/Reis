from googleplaces import GooglePlaces, lang, ranking
import googlemaps
from passport_app.email_manager import send_error
from passport_app.models import *
import logging
from passport_app.print_exception import *

logger = logging.getLogger(__name__)

def __init(keyAPI, is_send_email = False):
    try:
        google_places = GooglePlaces(keyAPI)
        gmaps = googlemaps.Client(key=keyAPI)
    except Exception as e:
        if is_send_email:
            send_error(str(e))
        # logger.error(str(e))
        PrintException()

    return google_places, gmaps


def __get_places(google_places_obj, gmaps, address_coord, term, radius, lang, is_send_email = False):
    try:
        # address_convert = gmaps.geocode(address)
        # address_coord = address_convert[0]['geometry']['location']
        logger.error(address_coord)
        
        query_result = google_places_obj.nearby_search(lat_lng=address_coord, language=lang, keyword=term, radius=radius) #language=lang.RUSSIAN, keyword=term, radius=radius)
        return len(query_result.places)
    except Exception as e:
        if is_send_email:
            send_error(str(e))
        PrintException()
        pass
    return 0

def __get_distanse(gmaps, google_places, address,placename,radius, lang, is_send_email = False):
    try:
        address_convert = gmaps.geocode(address)
        address_coord = address_convert[0]['geometry']['location']
        result_tr = google_places.nearby_search(location=address, language=lang, keyword=placename, radius=radius, rankby=ranking.DISTANCE)  #radius=10000,rankby=ranking.DISTANCE)
        
        if len(result_tr.places) > 0:
            near_place = result_tr.places[0].geo_location
            distwalk = gmaps.distance_matrix(address_coord, near_place, mode='walking')
            distance = distwalk['rows'][0]['elements'][0]['distance']['value']
            return distance
        
        return "";
    except Exception as e:
        if is_send_email:
            send_error(str(e))
        PrintException()
        pass
    return 0

def __get_lang(lang_code):
    if lang_code == "ru":
        return lang.RUSSIAN
    
    return lang.ENGLISH

def __get_parameter_name_by_lang(lang_code, param):
    if lang_code == "ru":
        return param.name_ru
    
    return param.name

def __save_to_parserparameter_data(real_estate, parser_parameter, value, is_send_email = False):
    try:
        parser_parameter_data = ParserParameterData()
        parser_parameter_data.value = value
        parser_parameter_data.real_estate = real_estate
        parser_parameter_data.parser_parameter = parser_parameter
        parser_parameter_data.save()
    except Exception as e:
        if is_send_email:
            send_error(str(e))
        PrintException()

def __save_to_parameter_data(real_estate, parser_parameter, value, is_send_email = False):
    parser_parameter = ParserParameter.objects.get(name = parser_parameter.name)
    
    try:
        parameter = Parameter.objects.get(name_ru = parser_parameter.name_ru)
        parameter_data = ParameterData()

        parameter_data.value = value
        parameter_data.real_estate = real_estate
        parameter_data.parameter = parameter
        parameter_data.comment = 'google'
        parameter_data.save()
    except Exception as e:
        logger.error('Parameter not found in db:' + parser_parameter.name)
        logger.error(str(e))

def google_search(keyAPI, address, social_infr, transport_dist, real_estate, lang_code, is_send_email = False):
#    keyAPI = "AIzaSyBvNq50ytusjcn2Hmn4OitJCr6Zi_uwD94"
    
    google_places, gmaps = __init(keyAPI)
    logger.error("init")
    result = {}
    lang = __get_lang(lang_code)
    logger.error("get lang %s" % (lang))

    address_convert = gmaps.geocode(address)
    address_coord = address_convert[0]['geometry']['location']
    logger.error(address_coord)

    for item in social_infr:
        try:                
            item_lang_name = __get_parameter_name_by_lang(lang_code, item)
            count = __get_places(google_places, gmaps, address_coord, item_lang_name, 1000, lang)
            
            result[item.name] = count
            __save_to_parameter_data(real_estate, item, str(count), is_send_email=True)
        except Exception as e:
            if is_send_email:
                send_error(str(e))
            PrintException()
            #__save_to_parameter_data(real_estate, item, str(count), is_send_email=True)
        
    # for item in transport_dist:
    #     try:
    #         item_lang_name = __get_parameter_name_by_lang(lang_code, item)
    #         dist = __get_distanse(gmaps, google_places, address, item_lang_name, 10000, lang)    
    #         #__save_to_parameter_data(real_estate, item, str(count), is_send_email=True)
    #     except Exception as e:
    #         if is_send_email:
    #             send_error(str(e))
    #         PrintException()
            #__save_to_parameter_data(real_estate, item, str(count), is_send_email=True)
            
    return result