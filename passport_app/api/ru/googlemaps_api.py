from googleplaces import GooglePlaces, lang,ranking
import googlemaps
from passport_app.email_manager import send_error
import logging

logger = logging.getLogger(__name__)

KeyAPI = "AIzaSyBvNq50ytusjcn2Hmn4OitJCr6Zi_uwD94"

google_places = GooglePlaces(KeyAPI)
gmaps = gmaps = googlemaps.Client(key=KeyAPI)


def get_places(address, term, radius):
    query_result = google_places.nearby_search(location=address,language=lang.RUSSIAN, keyword=term,radius=radius)
    return len(query_result.places)

SocialInfr = {
    "college":"Высшее учебное заведение ВУЗ",
    "school":"Общеобразовательная Школа учебное заведение",
    "kindergarten":"Детский сад",
    "atheneum": "Читальный зал Билиблиотека Книги",
    "shop":"Магазин",
    "domestic_service":"Бытовые услуги Химчистка Отелье Ремонт обуви",
    "rest_space":"Городской парк",
    "sport_complex":"Спортинвый комплекс Фитнес",
    "sport_ground": "Спортивная площадка Воркаут",
    "playground":"Детская площадка",
    "polyclinic":"Поликлиника больница",
    "mall":"Торговый центр",
    "pharmacy":"Аптека",
    "cafe":"Пункт Общественного питания",
    "bank":"Банк",
    "water_place":"Водный объект",
    "theatre":"Театр",
    "religion_object":"Религиозный объект церковь",
    "ambulance":"Подстанция скорой помощи"
}

Transportdist = {"metro_stations":"Станция метро",
                 "light_subway_stations":"станция МЦК",
                 "stations_of_electric_trains":"Станция электропоездов",
                 "public_transport_stops":"Остановка общественного транспорта автобусы",
                 "distance_from_the_center":"Администрация города",
                 "parking_spaces_for_paid_and_intercepting_parking_lots":"Машиноместа платных и перехватывающих парковок",
                 "transport_highways":"Транспортные магистрали",
                 # "Расстояние до пожарной части":"пожарная часть"
                 }

results = {}

def get_distanse(address,placename):
    address_convert = gmaps.geocode(address)
    address_coord = address_convert[0]['geometry']['location']
    result_tr = google_places.nearby_search(location=address,language=lang.RUSSIAN, keyword=placename,radius=10000,rankby=ranking.DISTANCE)
    near_place = result_tr.places[0].geo_location
    distwalk = gmaps.distance_matrix(address_coord, near_place, mode='walking')
    distance = distwalk['rows'][0]['elements'][0]['distance']['value']
    return distance

def google_search(address, result, is_send_email = False):
    for name in SocialInfr:
        try:
            count = get_places(address, SocialInfr[name], 1000)
            result['social'][name] = count
        except Exception as e:
            if is_send_email:
                send_error(str(e))
            result['social'][name] = 0
            logger.error(str(e))
            pass
    for name in Transportdist:
        try:
            dist = get_distanse(address, Transportdist[name])
            result['transport'][name] = dist
        except Exception as e:
            if is_send_email:
                send_error(str(e))
            result['transport'][name] = 0
            logger.error(str(e))
            pass


