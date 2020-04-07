import requests
from passport_app.email_manager import send_error
import json


#test
API_KEY = "1d0afbd9-3cfa-492b-9d7b-cdf185c94175"


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

def get_distance_places(address):
    url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey=%s&geocode=%s' % (API_KEY, address)



def yandex_get_address_data(address, is_send_email = False):
    url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey=%s&geocode=%s&results=1' % (API_KEY, address)
    response = requests.get(url)

    country = ''
    province = ''
    province2 = ''
    locality = ''
    street = ''
    house = ''
    text_address = ''
    point = ''

    try:
        if response.status_code == 200:
            json_data = json.loads(response.text)
            geo_metadata = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components']

            for address_itmes in geo_metadata:
                if address_itmes['kind'] == 'country':
                    country = address_itmes['name']

                if address_itmes['kind'] == 'province' and province == '':
                    province = address_itmes['name']
                elif address_itmes['kind'] == 'province':
                    province2 = address_itmes['name']

                if address_itmes['kind'] == 'locality':
                    locality = address_itmes['name']

                if address_itmes['kind'] == 'street':
                    street = address_itmes['name']

                if address_itmes['kind'] == 'house':
                    house = address_itmes['name']

            text_address = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
            point = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    except Exception as e:
        if is_send_email:
            send_error(str(e))

    result = {
              "country": country,
              "province": province,
              "province2":province2,
              "locality":locality,
              "street": street,
              "house": house,
              "text_address": text_address,
              "point": point
              }

    return result



