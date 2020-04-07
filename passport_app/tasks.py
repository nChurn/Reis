from background_task import background
from django.utils import timezone
from passport_app.models import *

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

# @background(schedule=1)
def init_classifier():
    print("start init classifier")
    #classificator
    params = [
        {
            'name':'social',
            'point':'1.1',
            'name_ru': "Социальная инфраструктура",
            'descr': ''
        },

        {
            'name': 'transport',
            'point': '1.2',
            'name_ru': "Транспортная доступность",
            'descr': ''
        },
        {
            'name': 'place_info',
            'point': '1.3',
            'name_ru': "Характеристики местоположения",
            'descr': ''
        },
        {
            'name': 'rights',
            'point': '1.4',
            'name_ru': "Права и обременения",
            'descr': ''
        },
        {
            'name': 'architecture',
            'point': '1.5',
            'name_ru': "Архитектура и конструкции",
            'descr': ''
        },
        {
            'name': 'engsys',
            'point': '1.6',
            'name_ru': "Инженерные системы",
            'descr': ''
        },
        {
            'name': 'base',
            'point': '1.0',
            'name_ru': "Основные",
            'descr': ''
        },
    ]

    for item in params:
        classificator = Classifier(**item)
        classificator.save()
    print("finish init classifier")

# @background(schedule=timezone.now())
def init_type_of_value():
    #class TypeOfValue(models.Model):
    #name = models.CharField(max_length=255)
    print("start init type of value")
    params = [
        {
            'name': 'integer',
        },

        {
            'name': 'float',
        },
        {
            'name': 'text',
        },
        {
            'name': 'date',
        },
        {
            'name': 'datetime',
        },
    ]

    for item in params:
        type_of_val = TypeOfValue(**item)
        type_of_val.save()
    print("finish init type of value")


# @background(schedule=timezone.now())
def init_units():
    print("start init unit")
    #name = models.CharField(max_length=255)

    params = [

    ]

    for item in params:
        unit = Unit(**item)
        unit.save()
    print("finish init unit")


# @background(schedule=timezone.now())
def init_addreses():
    print("start init country")
    # address
    country = Country(**{'name': 'Россия'})
    country.save()
    print("finish init classifier")

# @background(schedule=timezone.now())
def init_social_fields():
    print("start init fields")
    #social
    # name = models.CharField(max_length=255)
    # title = models.CharField(max_length=255)
    # title_rus = models.CharField(max_length=255)
    # unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # classifier = models.ForeignKey(Сlassifier, on_delete=models.CASCADE)
    params = [
        {
            'name':'college',
            'title':'college',
            'title_rus': "Высшее учебное заведение",
        },

        {
            'name': 'school',
            'title': 'school',
            'title_rus': "Общеобразовательная Школа учебное заведение",
        },
        {
            'name': 'kindergarten',
            'title': 'kindergarten',
            'title_rus': "Детский сад",
        },
        {
            'name': 'atheneum',
            'title': 'library',
            'title_rus': "Читальный зал Билиблиотека Книги",
        },
        {
            'name': 'shop',
            'title': 'college',
            'title_rus': "Высшее учебное заведение",
        },
        {
            'name': 'college',
            'title': 'shop',
            'title_rus': "Магазин",
        },
        {
            'name': 'domestic_service',
            'title': 'domestic service',
            'title_rus': "Бытовые услуги",
        },
        {
            'name': 'rest_space',
            'title': 'rest space',
            'title_rus': "Городской парк",
        },
        {
            'name': 'sport_complex',
            'title': 'sport_complex',
            'title_rus': "Спортинвый комплекс",
        },
        {
            'name': 'sport_ground',
            'title': 'sport ground',
            'title_rus': "Спортивная площадка",
        },
        {
            'name': 'playground',
            'title': 'playground',
            'title_rus': "Детская площадка",
        },
        {
            'name': 'polyclinic',
            'title': 'polyclinic',
            'title_rus': "Поликлиника больница",
        },
        {
            'name': 'mall',
            'title': 'mall',
            'title_rus': "Торговый центр",
        },
        {
            'name': 'college',
            'title': 'college',
            'title_rus': "Высшее учебное заведение",
        },
        {
            'name': 'pharmacy',
            'title': 'pharmacy',
            'title_rus': "Аптека",
        },
        {
            'name': 'cafe',
            'title': 'cafe',
            'title_rus': "Пункт Общественного питания",
        },
        {
            'name': 'bank',
            'title': 'bank',
            'title_rus': "Банк"
        },
        {
            'name': 'water_place',
            'title': 'water object',
            'title_rus': "Водный объект",
        },
        {
            'name': 'theatre',
            'title': 'theatre',
            'title_rus': "Театр",
        },
        {
            'name': 'religion_object',
            'title': 'religion_object',
            'title_rus': "Религиозный объект",
        },
        {
            'name': 'ambulance',
            'title': 'ambulance',
            'title_rus': "Подстанция скорой помощи",
        },

    ]



    classificator = Classifier.objects.get(name='social')
    for item in params:
        field = Field(**item)
        field.classifier = classificator
        field.save()

    print("finish init fields")

# @background(schedule=timezone.now())
def init_transport_fields():
    print("start init fields")
    #social
    # name = models.CharField(max_length=255)
    # title = models.CharField(max_length=255)
    # title_rus = models.CharField(max_length=255)
    # unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # classifier = models.ForeignKey(Сlassifier, on_delete=models.CASCADE)
    params = [
        {
            'name':'metro_stations',
            'title':'metro stations',
            'title_rus': "Станция метро",
        },
        {
            'name': 'light_subway_stations',
            'title': 'light subway stations',
            'title_rus': "станция МЦК",
        },
        {
            'name': 'stations_of_electric_trains',
            'title': 'stations_of_electric_trains',
            'title_rus': "Станция электропоездов",
        },
        {
            'name': 'public_transport_stops',
            'title': 'public_transport_stops',
            'title_rus': "Остановка общественного транспорта автобусы",
        },
        {
            'name': 'distance_from_the_center',
            'title': 'distance_from_the_center',
            'title_rus': "Администрация города",
        },
        {
            'name': 'parking_spaces_for_paid_and_intercepting_parking_lots',
            'title': 'parking_spaces_for_paid_and_intercepting_parking_lots',
            'title_rus': "Машиноместа платных и перехватывающих парковок",
        },
        {
            'name': 'transport_highways',
            'title': 'transport_highways',
            'title_rus': "Транспортные магистрали",
        },


    ]



    classificator = Classifier.objects.get(name='transport')
    for item in params:
        field = Field(**item)
        field.classifier = classificator
        field.save()

    print("finish init fields")


# @background(schedule=timezone.now())
def init_place_info_fields():
    print("start init fields")
    #social
    # name = models.CharField(max_length=255)
    # title = models.CharField(max_length=255)
    # title_rus = models.CharField(max_length=255)
    # unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # classifier = models.ForeignKey(Сlassifier, on_delete=models.CASCADE)
    params = [
        {
            'name':'location',
            'title':'location',
            'title_rus': "Местоположение",
        },
        {
            'name': 'area',
            'title': 'area',
            'title_rus': "Район",
        },
        {
            'name': 'geology',
            'title': 'geology',
            'title_rus': "Геология",
        },
        {
            'name': 'snap_to_the_town_plan',
            'title': 'snap_to_the_town_plan',
            'title_rus': "Привязка к градостроительному плану",
        },
        {
            'name': 'cadastral_engineer',
            'title': 'cadastral_engineer',
            'title_rus': "Кадастровый инженер",
        },
        {
            'name': 'cadastral_number_of_the_block',
            'title': 'cadastral_number_of_the_block',
            'title_rus': "Кадастровый номер квартала",
        },
        {
            'name': 'data_of_the_cadastral_passport_of_the_land_plot',
            'title': 'data_of_the_cadastral_passport_of_the_land_plot',
            'title_rus': "Данные кадастрового паспорта земельного участка",
        },
        {
            'name': 'land_category',
            'title': 'land_category',
            'title_rus': "Категория земель",
        },
        {
            'name': 'kind_of_permitted_use',
            'title': 'kind_of_permitted_use',
            'title_rus': "Вид разрешённого использования",
        },
        {
            'name': 'the_accuracy_of_the_boundaries_of_the_land',
            'title': 'the_accuracy_of_the_boundaries_of_the_land',
            'title_rus': "Точность границ земельного участка",
        },
        {
            'name': 'the_area_of_​​the_land_plot',
            'title': 'the_area_of_​​the_land_plot',
            'title_rus': "Площадь земельного участка, входящего в состав общего имущества в многоквартирном доме",
        },
        {
            'name': 'area_of_​​parking_within_the_boundaries_of_the_land_plot',
            'title': 'area_of_​​parking_within_the_boundaries_of_the_land_plot',
            'title_rus': "Площадь парковки в границах земельного участка",
        },
        {
            'name': 'date_of_change_of_information_in_gkn',
            'title': 'date_of_change_of_information_in_gkn',
            'title_rus': "Дата изменения сведений в ГКН",
        },
        {
            'name': 'date_of_unloading_of_information_in_gkn',
            'title': 'date_of_unloading_of_information_in_gkn',
            'title_rus': "Дата выгрузки сведений из ГКН",
        },
        {
            'name': 'place_info_playground',
            'title': 'place_info_playground',
            'title_rus': "Детская площадка",
        },
        {
            'name': 'place_info_sportground',
            'title': 'place_info_sportground',
            'title_rus': "Спортивная площадка",
        },
        {
            'name': 'other_elements_of_improvement',
            'title': 'other_elements_of_improvement',
            'title_rus': "Иные элементы благоустройства",
        },
        {
            'name': 'place_info_improvement',
            'title': 'place_info_improvement',
            'title_rus': "Благоустройство",
        },
    ]



    classificator = Classifier.objects.get(name='place_info')
    for item in params:
        field = Field(**item)
        field.classifier = classificator
        field.save()

    print("finish init fields")



# @background(schedule=timezone.now())
def init_rights_fields():
    print("start init fields")
    #social
    # name = models.CharField(max_length=255)
    # title = models.CharField(max_length=255)
    # title_rus = models.CharField(max_length=255)
    # unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # classifier = models.ForeignKey(Сlassifier, on_delete=models.CASCADE)
    params = [
        {
            'name':'special_conditions_for_the_use_of_land',
            'title':'special_conditions_for_the_use_of_land',
            'title_rus': "Особые условия использования земельных участков",
        },
        {
            'name': 'special_conditions_for_environmental_protection',
            'title': 'special_conditions_for_environmental_protection',
            'title_rus': "Особые условия охраны окружающей среды",
        },
        {
            'name': 'information_on_the_inclusion_of_a_property_in_the_register_of_cultural_heritage_sites',
            'title': 'information_on_the_inclusion_of_a_property_in_the_register_of_cultural_heritage_sites',
            'title_rus': "Сведения о включении объекта недвижимости в реестр объектов культурного наследия",
        },
        {
            'name': 'other_special_conditions_of_use',
            'title': 'other_special_conditions_of_use',
            'title_rus': "Иные особые условия использования",
        },
        {
            'name': 'name_of_the_managing_organization',
            'title': 'name_of_the_managing_organization',
            'title_rus': "Наименование управляющей организации",
        },
        {
            'name': 'location_address',
            'title': 'location_address',
            'title_rus': "Адрес местоположения",
        },
        {
            'name': 'rights_head_of_organization',
            'title': 'rights_head_of_organization',
            'title_rus': "Глава организации",
        },
        {
            'name': 'contact_number',
            'title': 'contact_phone',
            'title_rus': "Контактный телефон",
        },
        {
            'name': 'email',
            'title': 'email',
            'title_rus': "Почта",
        },
        {
            'name': 'official_website_of_the_company',
            'title': 'site',
            'title_rus': "Официальный сайт компании",
        },
        {
            'name': 'management_start_date',
            'title': 'management_start_date',
            'title_rus': "Дата начала управления",
        },
        {
            'name': 'management_document',
            'title': 'management_document',
            'title_rus': "Основание управления",
        },
        {
            'name': 'date_and_number_document',
            'title': 'date_and_number_document',
            'title_rus': "Дата и номер документа",
        },
        {
            'name': 'date_of_contract',
            'title': 'date_of_contract',
            'title_rus': "Дата заключения договора",
        },
        {
            'name': 'rate',
            'title': 'rate',
            'title_rus': "Тариф",
        },
        {
            'name': 'information_disclosure',
            'title': 'information_disclosure',
            'title_rus': "Раскрытие информации",
        },
        {
            'name': 'overhaul_schedule',
            'title': 'overhaul_schedule',
            'title_rus': "График капитального ремонта",
        },
        {
            'name': 'method_of_formation_of_the_capital_repair_fund',
            'title': 'method_of_formation_of_the_capital_repair_fund',
            'title_rus': "Способ формирования фонда капитального ремонта",
        },
        {
            'name': 'inn_account_owner',
            'title': 'inn_account_owner',
            'title_rus': "ИНН владельца специального счета",
        },
        {
            'name': 'amount_of_the_contribution_for_capital_repairs',
            'title': 'amount_of_the_contribution_for_capital_repairs',
            'title_rus': "Размер взноса на капитальный ремонт",
        },
        {
            'name': 'date_number_protocol',
            'title': 'date_number_protocol',
            'title_rus': "Дата и номер протокола собраний владельцев",
        },
        {
            'name': 'extra_info',
            'title': 'extra_info',
            'title_rus': "Дополнительная информация",
        },
        {
            'name': 'collected_means_of_owners_of_all',
            'title': 'collected_means_of_owners_of_all',
            'title_rus': "Собрано средств собственников всего",
        },
        {
            'name': 'current_debt_of_owners_on_contributions',
            'title': 'current_debt_of_owners_on_contributions',
            'title_rus': "Текущая задолженность собственников по взносам",
        },
        {
            'name': 'spent_on_work',
            'title': 'spent_on_work',
            'title_rus': "Израсходовано на работы",
        },
        {
            'name': 'including_spent_subsidies',
            'title': 'including_spent_subsidies',
            'title_rus': "В т.ч. израсходовано субсидий",
        },
        {
            'name': 'balance_of_funds_for_overhauling',
            'title': 'balance_of_funds_for_overhauling',
            'title_rus': "Остаток средств на проведение капремонта",
        },
        {
            'name': 'planned_works',
            'title': 'planned_works',
            'title_rus': "Запланировано работ",
        },
        {
            'name': 'completed_work',
            'title': 'completed_work',
            'title_rus': "Выполнено работ",
        },
        {
            'name': 'year_of_nearest_work',
            'title': 'year_of_nearest_work',
            'title_rus': "Год ближайшей работы",
        },
        {
            'name': 'management_report',
            'title': 'management_report',
            'title_rus': "Отчёт по управлению",
        },
        {
            'name': 'management_reports_archive',
            'title': 'management_reports_archive',
            'title_rus': "Архив отчетов по управлению",
        },
        {
            'name': 'debts_of_owners_before_the_criminal_code',
            'title': 'debts_of_owners_before_the_criminal_code',
            'title_rus': "Задолженность собственников перед УК",
        },

    ]



    classificator = Classifier.objects.get(name='rights')
    for item in params:
        field = Field(**item)
        field.classifier = classificator
        field.save()

    print("finish init fields")


# @background(schedule=timezone.now())
def init_architecture_fields():
    print("start init fields")
    #social
    # name = models.CharField(max_length=255)
    # title = models.CharField(max_length=255)
    # title_rus = models.CharField(max_length=255)
    # unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # classifier = models.ForeignKey(Сlassifier, on_delete=models.CASCADE)
    params = [
        {
            'name':'cadastral_number_of_the_building',
            'title':'cadastral_number_of_the_building',
            'title_rus': "Кадастровый номер здания",
        },
        {
            'name': 'cadastral_value_of_the_building',
            'title': 'cadastral_value_of_the_building',
            'title_rus': "Кадастровая стоимость здания",
        },
        {
            'name': 'date_of_cadastral_registration',
            'title': 'date_of_cadastral_registration',
            'title_rus': "Дата постановки на кадастровый учёт",
        },
        {
            'name': 'architecture_date_of_change_of_information_in_gkn',
            'title': 'date_of_unloading_of_information_in_gkn',
            'title_rus': "Дата изменения сведений в ГКН",
        },
        {
            'name': 'architecture_date_of_unloading_of_information_in_gkn',
            'title': 'date_of_unloading_of_information_in_gkn',
            'title_rus': "Дата выгрузки сведений из ГКН",
        },
        {
            'name': 'year_of_construction',
            'title': 'year_of_construction',
            'title_rus': "Год постройки",
        },
        {
            'name': 'year_of_commissioning',
            'title': 'metro stations',
            'title_rus': "Год ввода в эксплуатацию",
        },
        {
            'name': 'total_area',
            'title': '',
            'title_rus': "Общая площадь",
        },
         {
             'name': 'total_area_of_​​living_quarters',
             'title': '',
             'title_rus': "Общая площадь жилых помещений",
         },
         {
             'name': 'total_area_of_​​non_residential_premises',
             'title': '',
             'title_rus': "Общая площадь нежилых помещений",
         },
        {
            'name': 'total_area_of_​​premises_included_in_the_total_property',
            'title': '',
            'title_rus': "Общая площадь помещений, входящих в состав общего имущества",
        },
        {
            'name': 'number_of_storeys',
            'title': '',
            'title_rus': "Этажность",
        },
        {
            'name': 'number_of_residential_premises',
            'title': '',
            'title_rus': "Количество жилых помещений",
        },
        {
            'name': 'number_of_unresidential_premises',
            'title': '',
            'title_rus': "Количество нежилых помещений",
        },
        {
            'name': 'underground_floors',
            'title': '',
            'title_rus': "Подземных этажей",
        },
        {
            'name': 'functional_purpose_of_the_capital_construction_object',
            'title': '',
            'title_rus': "Функциональное назначение  объекта капитального строительства",
        },
        {
            'name': 'series_building_type',
            'title': '',
            'title_rus': "Серия, тип постройки здания",
        },
        {
            'name': 'type_of_house',
            'title': '',
            'title_rus': "Тип дома",
        },
        {
            'name': 'the_house_is_recognized_as_an_emergency',
            'title': '',
            'title_rus': "Дом признан аварийным",
        },
        {
            'name': 'type_of_foundation',
            'title': '',
            'title_rus': "Тип фундамента",
        },
        {
            'name': 'floor_type',
            'title': '',
            'title_rus': "Тип перекрытий",
        },
        {
            'name': 'material_of_bearing_walls',
            'title': '',
            'title_rus': "Материал несущих стен",
        },
        {
            'name': 'basement',
            'title': '',
            'title_rus': "Подвал",
        },
        {
            'name': 'basement_area',
            'title': '',
            'title_rus': "Площадь подвала",
        },
        {
            'name': 'number_of_entrances',
            'title': '',
            'title_rus': "Количество подъездов",
        },
        {
            'name': 'facade_type',
            'title': '',
            'title_rus': "Тип фасада",
        },
        {
            'name': 'roof_type',
            'title': '',
            'title_rus': "Тип крыши",
        },
        {
            'name': 'roofing_type',
            'title': '',
            'title_rus': "Тип кровли",
        },
        {
            'name': 'garbage_chute',
            'title': '',
            'title_rus': "Мусоропровод",
        },
        {
            'name': 'type_of_garbage_chute',
            'title': '',
            'title_rus': "Тип мусоропровода",
        },
        {
            'name': 'number_of_garbage_chutes',
            'title': '',
            'title_rus': "Количество мусоропроводов",
        },
        {
            'name': 'object_wear',
            'title': '',
            'title_rus': "Износ объекта",
        },
        {
            'name': 'conformity_of_the_building_with_ecological_gost_r_54964-2012',
            'title': '',
            'title_rus': "Соответствие здания экологическому ГОСТ Р 54964-2012",
        },
        {
            'name': 'inclusiveness',
            'title': '',
            'title_rus': "Инклюзивность",
        },


    ]



    classificator = Classifier.objects.get(name='architecture')
    for item in params:
        field = Field(**item)
        field.classifier = classificator
        field.save()

    print("finish init fields")


# @background(schedule=timezone.now())
def init_engsys_fields():
    print("start init fields")
    #social
    # name = models.CharField(max_length=255)
    # title = models.CharField(max_length=255)
    # title_rus = models.CharField(max_length=255)
    # unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # classifier = models.ForeignKey(Сlassifier, on_delete=models.CASCADE)
    params = [
        {
            'name':'external_networks',
            'title':'',
            'title_rus': "Внешние сети",
        },
        {
            'name': 'project_documentation',
            'title': '',
            'title_rus': "Проектная документация",
        },
        {
            'name': 'technical_documentation',
            'title': '',
            'title_rus': "Техническая документация",
        },
        {
            'name': 'energy_efficiency_class',
            'title': '',
            'title_rus': "Класс энергетической эффективности",
        },
        {
            'name': 'power_supply_system',
            'title': '',
            'title_rus': "Система электроснабжения",
        },
        {
            'name': 'type_of_power_supply_system',
            'title': '',
            'title_rus': "Тип системы электроснабжения",
        },
        {
            'name': 'number_of_entries_in_the_house',
            'title': '',
            'title_rus': "Количество вводов в дом",
        },
        {
            'name': 'the_fact_of_providing_the_supply_system_service',
            'title': '',
            'title_rus': "Факт предоставления услуги",
        },
        {
            'name': 'supply_system_rate',
            'title': '',
            'title_rus': "Тариф",
        },
        {
            'name': 'unit_of_supply_system_measurement',
            'title': '',
            'title_rus': "Единица измерения",
        },
        {
            'name': 'the_person_who_supplies_the_communal_supply_system_resource',
            'title': '',
            'title_rus': "Лицо, осуществляющее поставку коммунального ресурса",
        },
        {
            'name': 'date_of_installation_of_the_supply_meter',
            'title': '',
            'title_rus': "Дата установки прибора учёта",
        },
        {
            'name': 'type_of_supply_meter',
            'title': '',
            'title_rus': "Тип прибора учёта",
        },
        {
            'name': 'date_of_verification_replacement_of_the_supply_meter',
            'title': '',
            'title_rus': "Дата поверки / замены прибора учёта",
        },
        {
            'name': 'heat_supply_system',
            'title': '',
            'title_rus': "Система теплоснабжения",
        },
        {
            'name': 'type_of_heat_supply_system',
            'title': '',
            'title_rus': "Тип системы теплоснабжения",
        },
        {
            'name': 'the_fact_of_providing_the_heat_supply_service',
            'title': '',
            'title_rus': "Факт предоставления услуги",
        },
        {
            'name': 'unit_of_heat_supply_measurement',
            'title': '',
            'title_rus': "Единица измерения",
        },
        {
            'name': 'the_person_who_supplies_the_communal_heat_supply_resource',
            'title': '',
            'title_rus': "Лицо, осуществляющее поставку коммунального ресурса",
        },
        {
            'name': 'date_of_installation_of_the_heat_supply_meter',
            'title': '',
            'title_rus': "Дата установки прибора учёта",
        },
        {
            'name': 'type_of_heat_supply_meter',
            'title': '',
            'title_rus': "Тип прибора учёта",
        },
        {
            'name': 'date_of_verification_replacement_of_the_heat_supply_meter',
            'title': '',
            'title_rus': "Дата поверки / замены прибора учёта",
        },
        {
            'name': 'hot_water_system',
            'title': '',
            'title_rus': "Система горячего водоснабжения",
        },
        {
            'name': 'type_of_hot_water_system',
            'title': '',
            'title_rus': "Тип системы горячего водоснабжения",
        },
        {
            'name': 'the_fact_of_providing_the_hot_water_service',
            'title': '',
            'title_rus': "Факт предоставления услуги",
        },
        {
            'name': 'hot_water_rate',
            'title': '',
            'title_rus': "Тариф",
        },
        {
            'name': 'unit_of_hot_water_measurement',
            'title': '',
            'title_rus': "Единица измерения",
        },
        {
            'name': 'the_person_who_supplies_the_communal_hot_water_resource',
            'title': '',
            'title_rus': "Лицо, осуществляющее поставку коммунального ресурса",
        },
        {
            'name': 'date_of_installation_of_the_hot_water_meter',
            'title': '',
            'title_rus': "Дата установки прибора учёта",
        },
        {
            'name': 'type_of_hot_water_meter',
            'title': '',
            'title_rus': "Тип прибора учёта",
        },
        {
            'name': 'date_of_verification_replacement_of_the_hot_water_meter',
            'title': '',
            'title_rus': "Дата поверки / замены прибора учёта",
        },
        {
            'name': 'cold_water_system',
            'title': '',
            'title_rus': "Система холодного водоснабженияs",
        },
        {
            'name': 'type_of_cold_water_supply_system',
            'title': '',
            'title_rus': "Тип системы холодного водоснабжения",
        },
        {
            'name': 'the_fact_of_providing_the_cold_water_service',
            'title': '',
            'title_rus': "Факт предоставления услуги",
        },
        {
            'name': 'unit_of_cold_water_measurement',
            'title': '',
            'title_rus': "Единица измерения",
        },
        {
            'name': 'the_person_who_supplies_the_communal_cold_water_resource',
            'title': '',
            'title_rus': "Лицо, осуществляющее поставку коммунального ресурса",
        },
        {
            'name': 'date_of_verification_replacement_of_the_cold_water_metermeter',
            'title': '',
            'title_rus': "Дата поверки / замены прибора учёта",
        },
        {
            'name': 'type_of_cold_water_meter',
            'title': '',
            'title_rus': "Тип прибора учёта",
        },
        {
            'name': 'water_disposal_system',
            'title': '',
            'title_rus': "Система водоотведения",
        },
        {
            'name': 'type_of_sewerage_system',
            'title': '',
            'title_rus': "Тип системы водоотведения",
        },
        {
            'name': 'the_fact_of_providing_the_disposal_service',
            'title': '',
            'title_rus': "Факт предоставления услуги",
        },
        {
            'name': 'disposal_rate',
            'title': '',
            'title_rus': "Тариф",
        },
        {
            'name': 'unit_of_disposal_measurement',
            'title': '',
            'title_rus': "Единица измерения",
        },
        {
            'name': 'the_person_who_supplies_the_communal_disposal_resource',
            'title': '',
            'title_rus': "Лицо, осуществляющее поставку коммунального ресурса",
        },
        {
            'name': 'date_of_installation_of_the_disposal_meter',
            'title': '',
            'title_rus': "Дата установки прибора учёта",
        },
        {
            'name': 'type_of_disposal_meter',
            'title': '',
            'title_rus': "Тип прибора учёта",
        },
        {
            'name': 'date_of_verification_replacement_of_the_disposal_meter',
            'title': '',
            'title_rus': "Дата поверки / замены прибора учёта",
        },
        {
            'name': 'volume_of_cesspools',
            'title': '',
            'title_rus': "Объем выгребных ям",
        },
        {
            'name': 'gutter_system',
            'title': '',
            'title_rus': "Система водостоков",
        },
        {
            'name': 'gutter_system_type',
            'title': '',
            'title_rus': "Тип системы водостоков",
        },
        {
            'name': 'gas_supply_system',
            'title': '',
            'title_rus': "Система газоснабжения",
        },
        {
            'name': 'type_of_gas_supply_system',
            'title': '',
            'title_rus': "Тип системы газоснабжения",
        },
        {
            'name': 'the_fact_of_providing_the_gas_service',
            'title': '',
            'title_rus': "Факт предоставления услуги",
        },
        {
            'name': 'gas_supply_system_rate',
            'title': '',
            'title_rus': "Тариф",
        },
        {
            'name': 'unit_of_gas_measurement',
            'title': '',
            'title_rus': "Единица измерения",
        },
        {
            'name': 'the_person_who_supplies_the_communal_gas_resource',
            'title': '',
            'title_rus': "Лицо, осуществляющее поставку коммунального ресурса",
        },
        {
            'name': 'date_of_installation_of_the_gas_meter',
            'title': '',
            'title_rus': "Дата установки прибора учёта",
        },
        {
            'name': 'type_of_gas_meter',
            'title': '',
            'title_rus': "Тип прибора учёта",
        },
        {
            'name': 'date_of_verification_replacement_of_the_gas_meter',
            'title': '',
            'title_rus': "Дата поверки / замены прибора учёта",
        },
        {
            'name': 'ventilation_system',
            'title': '',
            'title_rus': "Система вентиляции",
        },
        {
            'name': 'type_of_ventilation_system',
            'title': '',
            'title_rus': "Тип системы вентиляции",
        },
        {
            'name': 'air_conditioning_system',
            'title': '',
            'title_rus': "Система кондиционирования",
        },
        {
            'name': 'weak_system',
            'title': '',
            'title_rus': "Слаботочная система",
        },
        {
            'name': 'lifting_equipment',
            'title': '',
            'title_rus': "Подъёмное оборудование",
        },
        {
            'name': 'type_of_lift',
            'title': '',
            'title_rus': "Тип лифта",
        },
        {
            'name': 'number_of_elevators',
            'title': '',
            'title_rus': "Количество лифтов",
        },
        {
            'name': 'year_of_commissioning_of_the_lift_system',
            'title': '',
            'title_rus': "Год ввода в эксплуатацию лифтовой системы",
        },
        {
            'name': 'integrated_security_system',
            'title': '',
            'title_rus': "Система комплексной безопасности",
        },
        {
            'name': 'video_surveillance',
            'title': '',
            'title_rus': "Видеонаблюдение",
        },
        {
            'name': 'fencing',
            'title': '',
            'title_rus': "Ограждение",
        },
        {
            'name': 'barrier',
            'title': '',
            'title_rus': "Шлагбаум",
        },
        {
            'name': 'integrated_fire_protection_system',
            'title': '',
            'title_rus': "Система комплексной противопожарной защиты",
        },
        {
            'name': 'fire_extinguishing_system',
            'title': '',
            'title_rus': "система пожаротушения",
        },
        {
            'name': 'type_fire_extinguishing_system',
            'title': '',
            'title_rus': "Тип системы пожаротушения",
        },
        {
            'name': 'distance_to_fire_station',
            'title': '',
            'title_rus': "Расстояние до пожарной части",
        },

    ]



    classificator = Classifier.objects.get(name='engsys')
    for item in params:
        field = Field(**item)
        field.classifier = classificator
        field.save()

    print("finish init fields")

# @background(schedule=timezone.now())
def create_config():
    print ("create config")
    try:
        count = SearchConfig.objects.count()
        if count == 0:
            search_config = SearchConfig()
            search_config.save()
    except Exception as e:
        print(str(e))
        pass

def move_data_to_category():
    #разделы

    razdel = Category()
    razdel.name = "razdel"
    razdel.point = "1.0"
    razdel.comment = ""
    razdel.name_ru = "Раздел"
    razdel.save()

    root_category = Category()
    root_category.name = "category"
    root_category.point = "1.0"
    root_category.comment = ""
    root_category.name_ru = "Категория"
    root_category.save()

    classifiers = Classifier.objects.all()

    for classifier in classifiers:
        try:
            category = Category()
            category.name = classifier.name
            category.point = classifier.point
            category.comment = classifier.descr
            category.name_ru = classifier.name_ru
            category.save()
            category.parent_categories.add(razdel)
            category.save()
            
            razdel.categories.add(category)
            razdel.save()
        except Exception as e:
            print(str(e))
            pass

    fields = Field.objects.all()

    for item in fields:
        try:
            category = Category()
            category.name = item.name                        
            category.name_ru = item.title_rus        
            category.save()
            if item.classifier:
                classifier_item = Category.objects.filter(name__exact =  item.classifier.name)
                if classifier_item:     
                    print ( "classifier_item %i" % classifier_item.count())               
                    print ( classifier_item )               
                    category.parent_categories.add(classifier_item[0])
                    classifier_item[0].categories.add(category)
                    classifier_item[0].save()
                else:
                    print ("not found classifier %s" % item.classifier.name )
            category.save()
            
            # parserparameter = ParserParameter()
            # parserparameter.name = item.name      
                              
            # # parameter.name_ru = item.title_rus  
            # # parameter.unit = item.unit       

            # parserparameter.save()
            # # category.parameters.add(parameter)
            # category.save()

            # field_data = DataField.objects.filter(field = item)
            # for field_data_item in field_data:
            #     print ("try save data parametter")
            #     data_parameter = ParserParameterData()
            #     data_parameter.value = field_data_item.value                        
            #     data_parameter.real_estate = field_data_item.real_estate
            #     data_parameter.parser_parameter = parserparameter                
            #     data_parameter.save()
            #     print ("save data parametter")

        except Exception as e:
            print(str(e))
            pass

    typeofrealestates = TypeOfRealEstate.objects.all()

    for item in typeofrealestates:
        try:
            category = Category()
            category.name = item.name
            category.name_ru = item.title_rus  
            category.save()
            category.parent_categories.add(root_category)
            category.save()
            root_category.categories.add(category)
            root_category.save()
        except Exception as e:
            print(str(e))
            pass

    subtypeofrealestates = SubtypeOfRealEstate.objects.all()

    for item in subtypeofrealestates:
        try:
            category = Category()
            category.name = item.name
            category.name_ru = item.title_rus
            category.save()
            if item.type:
                type_categories = Category.objects.filter(name__exact = item.type.name)
                if type_categories:
                    print ( "type_categories %i " % type_categories.count())
                    print ( type_categories )
                    category.parent_categories.add(type_categories[0])
                    type_categories[0].categories.add(category)
                    type_categories[0].save()
                else:
                    print ("not found type %s" % item.type.name )

            category.save()
        except Exception as e:
            print(str(e))
            pass

    subsubtypeofrealestates = SubsubtypeOfRealEstate.objects.all()

    for item in subsubtypeofrealestates:
        try:
            category = Category()
            category.name = item.name
            category.name_ru = item.title_rus
            category.save()
            if item.subtype:                
                subtype_categories = Category.objects.filter(name = item.subtype.name)
                if subtype_categories:
                    print ( "subtype_categories %i " % subtype_categories.count())
                    print ( subtype_categories )
                    category.parent_categories.add(subtype_categories[0])
                    subtype_categories[0].categories.add(category)   
                    subtype_categories[0].save()                 
                else:
                    print ("not found subtype %s" % item.subtype.name )
            category.save()
        except Exception as e:
            print(str(e))
            pass
            

    subsubsubtypeofrealestates = SubsubsubtypeOfRealEstate.objects.all()

    for item in subsubsubtypeofrealestates:
        try:
            category = Category()
            category.name = item.name
            category.name_ru = item.title_rus
            category.save()
            if item.subsubtype:
                subsubtype_categories = Category.objects.filter(name = item.subsubtype.name)
                if subsubtype_categories:
                    print ( "subsubtype_categories %i " % subsubtype_categories.count())
                    print ( subsubtype_categories )
                    category.parent_categories.add(subsubtype_categories[0])
                    subsubtype_categories[0].categories.add(category) 
                    subsubtype_categories[0].save()                   
                else:
                    print ("not found subsubtype %s" % item.subsubtype.name )
            category.save()
        except Exception as e:
            print(str(e))
            pass
            

def create_parser_types():
    print("create parser types...")
    parser_type = ParserType()
    parser_type.name = "google_map"
    parser_type.name_ru = "google map"
    parser_type.save()


    parser_type = ParserType()
    parser_type.name = "yandex_map"
    parser_type.name_ru = "yandex map"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "yandex_transport"
    parser_type.name_ru = "yandex transport"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "wiki_routes"
    parser_type.name_ru = "wiki routes"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "rosreestr.ru"
    parser_type.name_ru = "rosreestr.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "reformagkh.ru"
    parser_type.name_ru = "reformagkh.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "dom.gosuslugi.ru"
    parser_type.name_ru = "dom.gosuslugi.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "greenpatrol.ru"
    parser_type.name_ru = "greenpatrol.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "ecofactor.ru"
    parser_type.name_ru = "ecofactor.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "kartasvalok.ru"
    parser_type.name_ru = "kartasvalok.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "fssprus.ru"
    parser_type.name_ru = "fssprus.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "egrul.nalog.ru"
    parser_type.name_ru = "egrul.nalog.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "sudrf.ru"
    parser_type.name_ru = "sudrf.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "notariat.ru"
    parser_type.name_ru = "notariat.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "genproc.gov.ru"
    parser_type.name_ru = "genproc.gov.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "мвд.рф"
    parser_type.name_ru = "мвд.рф"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "mchs.gov.ru"
    parser_type.name_ru = "mchs.gov.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "rosinv.ru/o-predpriyatii"
    parser_type.name_ru = "rosinv.ru/o-predpriyatii"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "bti-moscow.ru"
    parser_type.name_ru = "bti-moscow.ru"
    parser_type.save()

    parser_type = ParserType()
    parser_type.name = "mobti.ru"
    parser_type.name_ru = "mobti.ru"
    parser_type.save()

    print("finished")

def create_parser_parameters():
    print("create parser parameters...")
    fields = Field.objects.all()
    for item in fields:
        try:
            
            parserparameter = ParserParameter()
            parserparameter.name = item.name      
                              
            parserparameter.name_ru = item.title_rus  
            parserparameter.parser_type = ParserType.objects.get(id = item.parser_type)
            parserparameter.save()

            field_data = DataField.objects.filter(field = item)
            for field_data_item in field_data:
                print ("try save data parametter")
                data_parameter = ParserParameterData()
                data_parameter.value = field_data_item.value                        
                data_parameter.real_estate = field_data_item.real_estate
                data_parameter.parser_parameter = parserparameter                
                data_parameter.save()
                print ("save data parametter")

        except Exception as e:
            print(str(e))
            pass
    print("finished")

def create_formula():
    print("create empty formulas")
    categories = Category.objects.all()
    for category in categories:
        try:        
            print ("try save data category formula")    
            category_formula = FormulaCategory() 
            category_formula.category = category
            category_formula.value_label = "FV_%i" % (category.id,)
            category_formula.rate_label = "FR_%i" % (category.id,)
            category_formula.formula_lbl = "FF_%i" % (category.id,)
            category_formula.save()
            print ("save data category formula")
            print (category.parameters)
            if category.parameters.exists():
                for parameter in category.parameters.all():
                    print ("try save data parametter formula")
                    parameter_formula = FormulaParameterCategory()
                    parameter_formula.category = category
                    parameter_formula.parameter = parameter
                    parameter_formula.value_label = "PV_%i_%i" % (parameter.id,category.id,)
                    parameter_formula.rate_label = "PR_%i_%i" % (parameter.id,category.id,)
                    parameter_formula.formula_label = "PF_%i_%i" % (parameter.id,category.id,)
                    parameter_formula.value = "PV_%i_%i" % (parameter.id,category.id,)
                    parameter_formula.rate = "PR_%i_%i" % (parameter.id,category.id,)         
                    parameter_formula.save()
                    print ("save data parametter formula")

        except Exception as e:
            print(str(e))
            pass
    print("finished")

def create_default_search_form():
    # if not SearchForm.objects.get(name = 'default'):
    search_form = SearchForm()
    search_form.name = 'default'
    search_form.name_ru = 'Стандартный'
    search_form.user = User.objects.get(id = 1)
    search_form.save()
    search_form.categories.set(Category.objects.all())
    
    search_form.save()



def init_db():
    con = psycopg2.connect(dbname='postgres',
      user='postgres', host='',
      password='postgres')

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

    cur = con.cursor()

    # Use the psycopg2.sql module instead of string concatenation 
    # in order to avoid sql injection attacs.
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier('db_passport'))
        )

def create_yandex_parameter():
    parser_type = ParserType.objects.filter(name = "google_map").first()
    parser_type_yandex = ParserType.objects.filter(name = "yandex_map").first()
    parser_parameters = ParserParameter.objects.filter(parser_type = parser_type)
    print("create_yandex_parameter")
    print(parser_type.name)
    print(parser_type_yandex.name)

    for item in parser_parameters:
        parserparameter = ParserParameter()
        parserparameter.name = item.name +"yandex"                                 
        parserparameter.name_ru = item.name_ru  
        parserparameter.parser_type = parser_type_yandex
        parserparameter.parser_parameter_type = item.parser_parameter_type
        parserparameter.save()

def tasks():
    print("tasks")
    # init_classifier()
    # init_addreses()
    # init_units()

    # init_type_of_value()
    # init_social_fields()
    # init_transport_fields()
    # init_place_info_fields()
    # init_architecture_fields()
    # init_rights_fields()

    # init_engsys_fields()
    # create_config()
    # move_data_to_category()
    # create_parser_types()
    # create_parser_parameters()
    # create_formula()
    # init_db()
    # create_default_search_form()
    create_yandex_parameter()
    # create_gkh_parameter()

    print("finish tasks")

# init_classifier()
