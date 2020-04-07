# from passport_app.parser.ru.rosreestr_ru_api import selenium_rosreestr
from passport_app.parser.ru.rosreestr_ru_parser import rosreestr_ru_parser
from passport_app.parser.ru.reforma_gkh_parser import search

def _get_data_from_rosreestr_ru(cn, address):
    #kadastr_number = "77:03:0003019:72"

    result = None
    # result = selenium_rosreestr(cn)
    result = rosreestr_ru_parser(cn)
    # address = "обл. Нижегородская, г. Нижний Новгород, б-р. Мира, д. 12"  #"Например: Нижегородская область Нижний Новгород Мира 12"
    gkh_result_doc, result_json, result_arch, result_place_char = search(address)
    return result, result_json, result_arch, result_place_char

def _get_data_from_reformagkh_by_address(address, result):
    gkh_result_doc = search(address, result)


def get_data_by_address(address, result):
    _get_data_from_reformagkh_by_address(address, result)


