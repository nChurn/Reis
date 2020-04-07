from datetime import datetime

import os
from pyquery import PyQuery as pq, PyQuery
# from estp.items import result
import uuid
from urllib.request import urlopen

import codecs
from datetime import datetime
from urllib.parse import urlencode
# from grab import Grab
import requests
from bs4 import BeautifulSoup

# from estp.items import result, copy_of_passport_dc, encumbrances_dc
# from estp.help_functions import convert_search_string_for_reformagkh, \
#     handleString
# from estp.reformagkh_part import handle_reformagkh_content
# from estp.rosrestr_part import click_address
# from estp.selenium_rosreestr import selenium_rosreestr


def handle_reformagkh_content(soup, result):
    list_span = soup.select('.col_list td span')
    for i in list_span:
        span_element = i.getText()
        parent_element_text = ""
        try:
            parent_element_text = i.parent.parent.findNext('tr').find('span').getText() #i.parent().parent().next()('span').text()
        except (KeyError, TypeError, AttributeError):
            pass
        if span_element.find(
                u'площадь земельного участка, входящего в состав общего имущества в многоквартирном доме, кв.м') != -1:
            result['place_info']['the_area_of_​​the_land_plot'] = parent_element_text
        if span_element.find(
                u'площадь парковки в границах земельного участка, кв.м') != -1:
            result['place_info']['area_of_​​parking_within_the_boundaries_of_the_land_plot'] = parent_element_text
        if span_element.find(u'детская площадка') != -1:
            result['place_info']['place_info_playground'] = parent_element_text
        if span_element.find(u'спортивная площадка') != -1:
            result['place_info']['place_info_sportground'] = parent_element_text
        if span_element.find(u'другое') != -1:  # Иные элементы благоустройства
            result['place_info']['other_elements_of_improvement'] = parent_element_text
        if span_element.find(u'общая площадь жилых помещений, кв.м') != -1:
            result['architecture']['total_area_of_​​living_quarters'] = parent_element_text
        if span_element.find(u'общая площадь нежилых помещений, кв.м') != -1:
            result['architecture']['total_area_of_​​non_residential_premises'] = parent_element_text
        if span_element.find(
                u'общая площадь помещений, входящих в состав общего имущества, кв.м') != -1:
            result['architecture']['the_total_area_of_​​premises_included_in_the_total_property'] = parent_element_text
        if span_element.find(u'Серия, тип постройки здания') != -1:
            result['architecture']['series_building_type'] = parent_element_text
        if span_element.find(u'Тип дома') != -1:
            result['architecture']['type_of_house'] = parent_element_text
        if span_element.find(
                u'Способ формирования фонда капитального ремонта') != -1:
            result['rights']['method_of_formation_of_the_capital_repair_fund'] = parent_element_text
        if span_element.find(u'Дом признан аварийным') != -1:
            result['architecture']['the_house_is_recognized_as_an_emergency'] = parent_element_text
        if span_element.find(u'Тип фундамента') != -1:
            result['architecture']['type_of_foundation'] = parent_element_text
        if span_element.find(u'Тип перекрытий') != -1:
            result['architecture']['floor_type'] = parent_element_text
        if span_element.find(u'Материал несущих стен') != -1:
            result['architecture']['material_of_bearing_walls'] = parent_element_text
        if span_element.find(u'Количество подъездов, ед.') != -1:
            result['architecture']['number_of_entrances'] = parent_element_text
        if span_element.find(u'Площадь подвала по полу, кв.м') != -1:
            result['architecture']['basement_area'] = parent_element_text
            result['architecture']['basement'] = 'Имеется'  # Подвал
        else:
            result['architecture']['basement'] = 'Не имеется'
        if span_element.find(u'Тип мусоропровода') != -1:
            result['architecture']['type_of_garbage_chute'] = parent_element_text
        if span_element.find(u'Количество мусоропроводов, ед.') != -1:
            result['architecture']['number_of_garbage_chutes'] = parent_element_text
            result['architecture']['garbage_chute'] = 'Имеется'  # Мусоропровод
        else:
            result['architecture']['garbage_chute'] = 'Не имеется'
        if span_element.find(u'Класс энергетической эффективности') != -1:
            result['engsys']['energy_efficiency_class'] = parent_element_text
        if span_element.find(u'Тип системы электроснабжения ') != -1:
            result['engsys']['type_of_power_supply_system'] = parent_element_text
        if span_element.find(u'Количество вводов в дом') != -1:
            result['engsys']['number_of_entries_in_the_house'] = parent_element_text
            result['engsys']['power_supply_system'] = 'Имеется'  # Система электроснабжения
        else:
            result['engsys']['power_supply_system'] = 'Не имеется'
        # Факт предоставления услуги
        if span_element.find(u'Тип системы теплоснабжения') != -1:
            result['engsys']['type_of_heat_supply_system'] = parent_element_text
            result['engsys']['heat_supply_system'] = 'Имеется'  # Система теплоснабжения
        else:
            result['engsys']['heat_supply_system'] = 'Не имеется'
        if span_element.find(u'Тип системы пожаротушения') != -1:
            result['engsys']['type_of_fire_extinguishing_system'] = parent_element_text
            result['engsys']['fire_extinguishing_system'] = 'Имеется'  # Система пожаротушения
        else:
            result['engsys']['fire_extinguishing_system'] = 'Не имеется'
        if span_element.find(u'Система горячего водоснабжения') != -1:
            result['engsys']['type_of_hot_water_system'] = parent_element_text
            result['engsys']['hot_water_system'] = 'Имеется'  # Горячее водоснаюжение
        else:
            result['engsys']['hot_water_system'] = 'Не имеется'
        if span_element.find(u'Тип системы холодного водоснабжения') != -1:
            result['engsys']['type_of_cold_water_supply_system'] = parent_element_text
            result['engsys']['cold_water_system'] = 'Имеется'
        else:
            result['engsys']['cold_water_system'] = 'Не имеется'
        if span_element.find(u'Тип системы водоотведения') != -1:
            result['engsys']['type_of_sewerage_system'] = parent_element_text
            result['engsys']['water_disposal_system'] = 'Имеется'  # Система водоотведения
        else:
            result['engsys']['water_disposal_system'] = 'Не имеется'
        if span_element.find(u'Тип системы водостоков') != -1:
            result['engsys']['gutter_system_type'] = parent_element_text
            result['engsys']['gutter_system'] = 'Имеется'  # Система водостоков
        else:
            result['engsys']['gutter_system'] = 'Не имеется'
        if span_element.find(u'Тип системы газоснабжения') != -1:
            result['engsys']['type_of_gas_supply_system'] = parent_element_text
            result['engsys']['gas_supply_system'] = 'Имеется'  # Система газоснабжения
        else:
            result['engsys']['gas_supply_system'] = 'Не имеется'
        if span_element.find(u'Тип системы вентиляции') != -1:
            result['engsys']['type_of_ventilation_system'] = parent_element_text
            result['engsys']['ventilation_system'] = 'Имеется'  # Система вентиляции
        else:
            result['engsys']['ventilation_system'] = 'Не имеется'
        if span_element.find(u'Объем выгребных ям, куб. м.') != -1:
            result['engsys']['volume_of_cesspools'] = parent_element_text

    # такие поля, как "дата установки прибора на учет/тип прибора учета/дата проверки прибора"
    def handlerField(i, text, date, type, replace):
        if pq(i)('td:nth-child(1)').text().find(text) != -1:
            date['information'] = pq(i)('td:nth-child(4)').text()
            for k in pq(i)('td:nth-child(1)').parent().next()(
                    'tr.left td span'):
                if pq(k).text().find(u'Тип прибора учета'):
                    type['information'] = pq(k).parent().parent().next()(
                        'td span').text()
                if pq(k).text().find(u'Дата поверки / замены прибора учета'):
                    replace['information'] = pq(k).parent().parent().next()(
                        'td span').text()

    soup_list = soup.select('#tab1-subtab5 div table tbody tr')
    
    result['engsys'] = {}
    result['engsys']['date_of_installation_of_the_heat_supply_meter'] = ''
    result['engsys']['type_of_heat_supply_meter'] = ''
    result['engsys']['date_of_verification_replacement_of_the_heat_supply_meter'] = ''
    result['engsys']['date_of_installation_of_the_supply_meter'] = ''
    result['engsys']['type_of_supply_meter'] = ''
    result['engsys']['date_of_verification_replacement_of_the_supply_meter'] = ''
    result['engsys']['date_of_installation_of_the_hot_water_meter'] = ''
    result['engsys']['type_of_hot_water_meter'] = ''
    result['engsys']['date_of_verification_replacement_of_the_hot_water_meter'] = ''
    result['engsys']['date_of_installation_of_the_cold_water_meter'] = ''
    result['engsys']['type_of_cold_water_meter'] = ''
    result['engsys']['date_of_verification_replacement_of_the_cold_water_metermeter'] = ''
    result['engsys']['date_of_installation_of_the_disposal_meter'] = ''
    result['engsys']['type_of_disposal_meter'] = ''
    result['engsys']['date_of_verification_replacement_of_the_disposal_meter'] = ''
    result['engsys']['date_of_installation_of_the_gas_meter'] = ''
    result['engsys']['type_of_gas_meter'] = ''
    result['engsys']['date_of_verification_replacement_of_the_gas_meter'] = ''

    for i in soup_list:
        handlerField(i.getText(), u'Отопление',
            result['engsys']['date_of_installation_of_the_heat_supply_meter'],
            result['engsys']['type_of_heat_supply_meter'],
            result['engsys']['date_of_verification_replacement_of_the_heat_supply_meter'])
        handlerField(i.getText(), u'Электроснабжение',
            result['engsys']['date_of_installation_of_the_supply_meter'],
            result['engsys']['type_of_supply_meter'],
            result['engsys']['date_of_verification_replacement_of_the_supply_meter'])
        handlerField(i.getText(), u'Горячее водоснабжение',
            result['engsys']['date_of_installation_of_the_hot_water_meter'],
            result['engsys']['type_of_hot_water_meter'],
            result['engsys']['date_of_verification_replacement_of_the_hot_water_meter'])
        handlerField(i.getText(), u'Холодное водоснабжение',
            result['engsys']['date_of_installation_of_the_cold_water_meter'],
            result['engsys']['type_of_cold_water_meter'],
            result['engsys']['date_of_verification_replacement_of_the_cold_water_metermeter'])
        handlerField(i.getText(), u'Водоотведение',
            result['engsys']['date_of_installation_of_the_disposal_meter'],
            result['engsys']['type_of_disposal_meter'],
            result['engsys']['date_of_verification_replacement_of_the_disposal_meter'])
        handlerField(i.getText(), u'Газоснабжение',
            result['engsys']['date_of_installation_of_the_gas_meter'],
            result['engsys']['type_of_gas_meter'],
            result['engsys']['date_of_verification_replacement_of_the_gas_meter'])

    # поля котоыре в таблицах с синей шапкой
    soup_list = soup.select('.grid th')
    for i in soup_list:
        span_element = i.getText()
        parent_element_text = i.parent.parent.findNext('thead').find('th').getText()
        if span_element.find(u'Тип фасада') != -1:
            result['architecture']['facade_type'] = parent_element_text
        if span_element.find(u'Тип крыши') != -1:
            result['architecture']['roof_type'] = pq(
                i).parent().parent().next()('td:first-child').text()
        if span_element.find(u'Тип кровли') != -1:
            result['architecture']['roofing_type'] = pq(
                i).parent().parent().next()('td:last-child').text()
        if span_element.find(u'Тип лифта') != -1:
            result['engsys']['type_of_lift'] = []
            result['engsys']['year_of_commissioning_of_the_lift_system'] = []
            # Тип лифта
            for tbody in soup.select(
                    '#tab1-subtab4 table.orders.overhaul-services-table tbody td:nth-child(3)'):
                result['engsys']['type_of_lift'].append(
                    pq(tbody).text())

            # Год ввода в эксплуатацию лифтовой системы
            for tbody in soup.select(
                    '#tab1-subtab4 table.orders.overhaul-services-table tbody td:nth-child(4)'):
                result['engsys']['year_of_commissioning_of_the_lift_system'].append(pq(tbody).text())

            result['engsys']['number_of_elevators'] = len(
                result['engsys']['type_of_lift'])  # Количество лифтов

            if (result['engsys']['number_of_elevators'] > 0):
                result['engsys']['lifting_equipment'] = 'Имеется' # Подъемное оборудование
            else:
                result['engsys']['lifting_equipment'] = 'Не имеется'

    # График капитального ремонта
    house_list = soup.select('.banner-title-location > .location_banner')
    house = ""
    if house_list:
        house = house_list.attr('data-span-filter')
    if (house == 'house'):
        result['rights'] = {}
        result['rights']['overhaul_schedule'] = 'Имеется'
    else:
        result['rights'] = {}
        result['rights']['overhaul_schedule'] = 'Не имеется'

    # переход в вкладку "управление"
    management_link = ''
    finance_link = ''
    for tab in soup.select('.tab_labels.bordered li a'):
        if pq(tab).text().find(u'Управление') != -1:
            management_link = 'https://www.reformagkh.ru' + pq(tab).attr('href')
        if pq(tab).text().find(u'Отчеты по управлению') != -1:
            finance_link = 'https://www.reformagkh.ru' + pq(tab).attr('href')
    docs = []
    # g.go(management_link)
    if management_link:
        page = requests.get(management_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        # созраняем pdf файлы
        docs = []

        for i in soup.select('tbody tr td'):
            if pq(i).text().find(u'Добавлено (обновлено)') == 0:

                pdf_link = 'https://www.reformagkh.ru' + pq(i).parent()('td:nth-child(1) > a').attr('href')
                pdf_name = pq(i).parent()('td:nth-child(1) > a').text().replace(" ", "").replace("\n", "")

                # уникальное имя файла
                unique_filename = uuid.uuid4().int>>64
                pdf_path = '../media/docs/e%s.pdf' % unique_filename

                # создать папки в пути, если не существуют
                os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                docs.append([pdf_name, pdf_path])

                response = urlopen(pdf_link)
                file = open(pdf_path, 'wb')
                file.write(response.read())
                file.close()

        # поля с тарифами, еденицей измерения, лицом поставки, факт предоставления услуги
        for td in soup.select('.orders.overhaul-services-table tr.middle td'):

            if pq(td).text().find(u'Газоснабжение') != -1:
                # Факт предоставления услуги
                result['engsys']['the_fact_of_providing_the_gas_service'] = pq(td).next().text()
                # Тариф
                result['engsys']['gas_supply_system_rate'] = pq(
                    td).next().next().text() + ' руб'
                # Еденица измерения
                result['engsys']['unit_of_gas_measurement'] = pq(
                    td).next().next().next().text()
                # Лицо, осуществляющее поставку коммунального ресурса
                result['engsys']['the_person_who_supplies_the_communal_gas_resource'] = pq(td).next().next().next().next().text()

            if pq(td).text().find(u'Водоотведение') != -1:
                # Факт предоставления услуги
                result['engsys']['the_fact_of_providing_the_disposal_service'] = pq(td).next().text()
                # Тариф
                result['engsys']['disposal_rate'] = pq(
                    td).next().next().text() + ' руб'
                # Еденица измерения
                result['engsys']['unit_of_disposal_measurement'] = pq(
                    td).next().next().next().text()
                # Лицо, осуществляющее поставку коммунального ресурса
                result['engsys']['the_person_who_supplies_the_communal_disposal_resource'] = pq(td).next().next().next().next().text()

            if pq(td).text().find(u'Холодное водоснабжение') != -1:
                # Факт предоставления услуги
                result['engsys']['the_fact_of_providing_the_cold_water_service'] = pq(td).next().text()
                # Тариф
                result['engsys']['cold_water_rate'] = pq(
                    td).next().next().text() + ' руб'
                # Еденица измерения
                result['engsys']['unit_of_cold_water_measurement'] = pq(
                    td).next().next().next().text()
                # Лицо, осуществляющее поставку коммунального ресурса
                result['engsys'][
                    'the_person_who_supplies_the_communal_cold_water_resource'] = pq(td).next().next().next().next().text()

            if pq(td).text().find(u'Горячее водоснабжение') != -1:
                # Факт предоставления услуги
                result['engsys']['the_fact_of_providing_the_hot_water_service'] = pq(td).next().text()
                # Тариф
                result['engsys']['hot_water_rate']= pq(
                    td).next().next().text() + ' руб'
                # Еденица измерения
                result['engsys']['unit_of_hot_water_measurement'] = pq(
                    td).next().next().next().text()
                # Лицо, осуществляющее поставку коммунального ресурса
                result['engsys'][
                    'the_person_who_supplies_the_communal_hot_water_resource'] = pq(td).next().next().next().next().text()

            if pq(td).text().find(u'Электроснабжение') != -1:
                # Факт предоставления услуги
                result['engsys']['the_fact_of_providing_the_supply_system_service'] = pq(td).next().text()
                # Тариф
                result['engsys']['supply_system_rate']['information'] = pq(
                    td).next().next().text() + ' руб'
                # Еденица измерения
                result['engsys']['unit_of_supply_system_measurement'] = pq(
                    td).next().next().next().text()
                # Лицо, осуществляющее поставку коммунального ресурса
                result['engsys'][
                    'the_person_who_supplies_the_communal_supply_system_resource'] = pq(td).next().next().next().next().text()

            if pq(td).text().find(u'Отопление') != -1:
                # Факт предоставления услуги
                result['engsys']['the_fact_of_providing_the_heat_supply_service'] = pq(td).next().text()
                # Тариф
                result['engsys']['heat_supply_rate'] = pq(
                    td).next().next().text() + ' руб'
                # Еденица измерения
                result['engsys']['unit_of_heat_supply_measurement'] = pq(
                    td).next().next().next().text()
                # Лицо, осуществляющее поставку коммунального ресурса
                result['engsys'][
                    'the_person_who_supplies_the_communal_heat_supply_resource'] = pq(td).next().next().next().next().text()

    # переход в вкладку "финансы"
    # g.go(finance_link)
    if finance_link:
        page = requests.get(finance_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        for i in soup.select('.col_list td span'):
            span_element = pq(i).text()
            parent_element_text = pq(i).parent().parent().next()('span').text()
            if span_element.find(
                    u'денежных средств от собственников/нанимателей помещений, руб.') != -1:
                result['rights']['collected_means_of_owners_of_all'] = parent_element_text + ' руб'
            if span_element.find(
                    u'Начислено за услуги (работы) по содержанию и текущему ремонту, в том числе:') != -1:
                result['rights']['spent_on_work'] = parent_element_text + ' руб'
            if span_element.find(u'субсидий, руб.') != -1:
                result['rights']['including_spent_subsidies'] = parent_element_text + ' руб'
            if span_element.find(
                    u'Переходящие остатки денежных средств (на конец периода), руб.') != -1:
                result[rights]['including_spent_subsidies'] = parent_element_text + ' руб'

        # Отчёт по управлению
        if soup.select(
                '#house-management-info-block .black_text strong').text().find(
                u'Выберите отчетный период: '):
            result['rights']['management_report'] = 'Имеется'
            result['rights']['management_reports_archive'] = 'Имеется'
        else:
            result['rights']['management_report'] = 'Не имеется'
            result['rights']['management_reports_archive'] = 'Не имеется'

        # самый первый блок правее карты
        developer_link = ''
        for i in soup.select(
                '.house_info.clearfix div.fr table.upper_text tr td'):
            if pq(i).text().find(
                    u'Домом управляет:') != -1:  # получаем ссылку на информацию о застройщике
                result['rights']['name_of_the_managing_organization'] = pq(i).next().text()
                developer_link = 'https://www.reformagkh.ru' + pq(i).next()(
                    'a').attr('href')

        # страница с информацией о застройщике
        # g.go(developer_link)
        page = requests.get(developer_link)
        soup = BeautifulSoup(page.content, 'html.parser')


        for i in soup.select('.fr p span.black_text strong'):
            p_element_text = pq(i).parent().parent().text()
            if pq(i).text().find(
                    u'Фактический адрес:') != -1:  # Адрес местоположения
                result['rights']['location_address'] = p_element_text.replace(u'Фактический адрес: ',
                    '')
            if pq(i).text().find(u'Официальный сайт в сети Интернет:') != -1:
                result['rights']['official_website_of_the_company'] = p_element_text.replace(
                    u'Официальный сайт в сети Интернет: ', '')
            if pq(i).text().find(u'Телефон и e-mail:') != -1:  # Телефон и e-mail
                telephone_email_array = p_element_text.replace(
                    u'Телефон и e-mail: ', '').split(',')
                try:
                    result['rights']['contact_number'] = \
                    telephone_email_array[0].strip()
                    result['rights']['email'] = telephone_email_array[
                        1].strip()
                except:
                    pass

        for i in soup.select('#tab1-subtab1 > div.grid tbody tr:nth-child(1)'):
            result['control_selection_method'] = pq(i)(
                'td:nth-child(3)').text()
            result['management_start_date'] = pq(i)(
                'td:nth-child(4)').text()

        # вернутся с страницы о застройщике в родительскую ссылку
        # g.go(finance_link)
        page = requests.get(finance_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Размер взноса на капитальный ремонт
        overhaul_link = ''
        for i in soup.select('#showOverhaulBannerModal'): #пройдемся по модальным окнам
            pq_i = pq(i)
            if (pq_i('.modal_title').text().find('Капитальный ремонт') != -1):
                overhaul_link = 'https://www.reformagkh.ru' + pq_i('.btn.fr').attr('href') # получаем линк на подробню инфу

        if (len(overhaul_link) > 0):
            result['information_disclosure'] = 'Имеется'
            # g.go(overhaul_link)
            page = requests.get(overhaul_link)
            soup = BeautifulSoup(page.content, 'html.parser')
            for i in soup.select('.house_info.clearfix > .bulletin.clearfix > div'):
                pq_i = pq(i)
                if (pq_i.text().find('Размер взноса на капитальный ремонт') != -1):
                    result['amount_of_the_contribution_for_capital_repairs'] = pq_i.children().text()
                if (pq_i.text().find('Текущая задолженность собственников по взносам') != -1):
                    result['current_debt_of_owners_on_contributions'] = pq_i.children().text()
                if (pq_i.text().find('Остаток средств на проведение капремонта') != -1):
                    result['balance_of_funds_for_overhauling'] = pq_i.children().text()
                if (pq_i.text().find('Запланировано работ') != -1):
                    result['planned_works'] = pq_i.children().text()
                if (pq_i.text().find('Год ближайшей работы') != -1):
                    result['year_of_nearest_work'] = pq_i.children().text()
                if (pq_i.text().find('Выполнено работ') != -1):
                    result['completed_work'] = pq_i.children().text()
        else:
            result['rights']['information_disclosure']= 'Не имеется'

        # Задолженность собственников перед УК
        passport_tab_link = overhaul_link.replace('services', 'view') #вкладка пасспорта
        # g.go(passport_tab_link)
        page = requests.get(passport_tab_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        for i in soup.select('#tab1 .table-details.table-numbered .leaders.number span'):
            pq_i = pq(i)
            if (pq_i.text().find('Текущая задолженность собственников по взносам на капитальный ремонт') != -1):
                result['rights']['debts_of_owners_before_the_criminal_code'] = 'Имеется'
            else:
                result['rights']['debts_of_owners_before_the_criminal_code'] = 'Не имеется'

    return docs

def convert_search_string_for_reformagkh(string):  # обработка поисковой строки для reformagkh
    string_array = string.lower().split(',')  # пример г. Москва, ул. Полярная, д. 54, корп. 3
    result_array = []
    for i in string_array:
        search_part = i.strip()
        if search_part.find(u'г.') == 0:
            result_array.append(search_part)
        if search_part.find(u'ул.') == 0:
            result_array.append(search_part)
        if search_part.find(u'д.') == 0:
            result_array.append(search_part)
        if search_part.find(u'к.') == 0:
            result_array.append(search_part)

    return ', '.join(result_array)


def search(address_string, result):

    # второй источник - reformagkh
    print("GKH address:"+address_string)
    docs_dc = {}
    params = {'all': 'on',
              'query': convert_search_string_for_reformagkh(address_string)}
    url_params = urlencode(params)
    url = 'https://www.reformagkh.ru/search/houses' + '?' + url_params
    print("GKH url:"+url)

    # g.go(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:  # получить ссылку из блока с результатами
        if soup.find('table'):
            house_link = 'https://www.reformagkh.ru' + soup.find('table').find('a', href=True)['href']
            page = requests.get(house_link)
            soup = BeautifulSoup(page.content, 'html.parser')
            docs_dc = handle_reformagkh_content(soup, result)  # записываем контет в массивы
    except TypeError:  # если в поиске найдено 0 результатов
        docs_dc = {}

    # в этом блоке использую повторно спарсеные поля
    # try:  # кадастровый номер здания (Данные кадастрового паспорта земельного участка для copy_of_passport)
    #     copy_of_passport_dc['data_of_the_cadastral_passport']['data'] = \
    #         result['cadastral_number_of_the_building']['information']
    #     handleString(copy_of_passport_dc['data_of_the_cadastral_passport'])
    # except KeyError:
    #     pass
    #
    # try:  # точность гоаниц
    #     copy_of_passport_dc['accuracy_of_land_boundaries']['data'] = \
    #         result['the_accuracy_of_the_boundaries_of_the_land'][
    #             'information']
    #     handleString(copy_of_passport_dc['accuracy_of_land_boundaries'])
    # except KeyError:
    #     pass
    #
    # try:  # местоположение (Адресс для copy_of_passport)
    #     copy_of_passport_dc['address']['data'] = result['location'][
    #         'information']
    #     handleString(copy_of_passport_dc['address'])
    # except KeyError:
    #     pass
    #
    # try:  # общая площадь (Площадь участка для copy_of_passport)
    #     copy_of_passport_dc['plottage']['data'] = result['total_area'][
    #         'information']
    #     handleString(copy_of_passport_dc['plottage'])
    # except (KeyError, TypeError, AttributeError):
    #     pass
    #
    # try:  # этажность (для copy_of_passport)
    #     copy_of_passport_dc['floors']['data'] = result['number_of_storeys'][
    #         'information']
    #     handleString(copy_of_passport_dc['floors'])
    # except (KeyError, TypeError):
    #     pass
    #
    # try:  # подземных этажей (для copy_of_passport)
    #     copy_of_passport_dc['including_the_underground_floors']['data'] = \
    #         result['underground_floors']['information']
    #     handleString(copy_of_passport_dc['including_the_underground_floors'])
    # except (KeyError, TypeError):
    #     pass
    #
    # try:  # Функциональное назначение объекта капитального строительства (для copy_of_passport)
    #     copy_of_passport_dc['functional_purpose_of_capital_construction'][
    #         'data'] = \
    #         result['functional_purpose_of_the_capital_construction_object'][
    #             'information']
    #     handleString(
    #         copy_of_passport_dc['functional_purpose_of_capital_construction'])
    # except (KeyError, TypeError):
    #     pass

    # print(result)

    return docs_dc

# search( "обл. Нижегородская, г. Нижний Новгород, б-р. Мира, д. 12")
# search( "г.Москва, пл.Славянская, д.4, стр.1")
# search( "Славянская пл , д. 4к1с1 , г Москва , г Москва")