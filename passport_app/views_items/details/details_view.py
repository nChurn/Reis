import json
import os
import pprint
import re
import sys

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import Group, User
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.db.models import Count, Value
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import *
from django.shortcuts import redirect, render, render_to_response
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.generic import *
from rest_framework import generics, permissions, viewsets
from rest_framework.request import Request

from passport_app.api.reestr_api import (
    get_data_from_rosreesr_api_by_address, get_data_from_rosreesr_api_by_cn)
from passport_app.api.ru.yandexmaps_api import *
from passport_app.data_sources.data_sources_manager import start_search_info
from passport_app.data_sources.DataSourcesLauncher import DataSourcesLauncher
from passport_app.email_manager import send_search_result
from passport_app.models import *
from passport_app.parser.parser_ru import get_data_by_address
from passport_app.print_exception import *
from passport_app.real_estate_manager import (create_new_by_old,
                                              create_new_real_estate,
                                              create_property_dict,
                                              update_real_estate)
from passport_app.serializers import *
from passport_app.views_items.ajaxview import *
from passport_app.views_items.category import *
from passport_app.views_items.parameters import *
from passport_app.views_items.property_types.subsubsubtypeofrealestate import *
from passport_app.views_items.search_settings import *
from passport_app.views_items.unit import *

from passport_app.calc.calc import *


class DetailsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'passport_app.view_classifier', 'passport_app.view_country',
        'passport_app.view_datafield', 'passport_app.view_district',
        'passport_app.view_field', 'passport_app.view_owner',
        'passport_app.view_region', 'passport_app.view_street',
        'passport_app.view_subtypeofrealestate', 'passport_app.view_locality',
        'passport_app.view_realestate', 'passport_app.view_typeofrealestate',
        'passport_app.view_typeofstreet', 'passport_app.view_typeofvalue',
        'passport_app.view_unit')
    template_name = 'details.html'

    def get_parameter_data(self, parameter, real_estate, formula):
        try:
            parameter_datas = ParameterData.objects.filter(
                parameter=parameter, real_estate=real_estate)
            
            val = 0
            rate = 0
            formula = 0
            id = 0
            result = []
            if parameter_datas.exists() and parameter_datas.count() > 0:
                parameter_data = parameter_datas[0]
                id = parameter_data.id
                val = parameter_data.value
                rate = parameter_data.rate
                formula = 0
            else:
                parameter_data = ParameterData()
                parameter_data.real_estate = RealEstate.objects.get(
                    id=real_estate.id)
                parameter_data.parameter = Parameter.objects.get(
                    id=parameter.id)
                parameter_data.save()
                id = parameter_data.id
                val = parameter_data.value
                rate = parameter_data.rate
                formula = 0

            if not val:            
                parser_parameters = parameter.parser_parameters
                if parser_parameters.exists() and parser_parameters.count() > 0:   
                    parser_parameter = parser_parameters[0]
                    val = parser_parameter.value

            
            if parameter_datas.exists() and parameter_datas.count() > 0:
                for param in parameter_datas:
                    result.append({
                        'id': param.id,
                        'val': param.value,
                        'rate': param.rate,
                        'formula': 0,
                        'name': param.parameter.name_ru +" "+ param.comment
                    })
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e))
            print(exc_type, fname, exc_tb.tb_lineno)

        return val, rate, formula, id, result

    def get_form_category_data(self, categories, real_estate):
        data = []
        try:
            if categories.exists():
                for cat in categories.extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                    order_by('int_point').all():
                    cat_data = {}
                    cat_data['category'] = cat
                    cat_data['point'] = cat.point
                    cat_data['formula'] = FormulaCategory.objects.filter(
                        category=cat).first()
                    cat_data['rate'] = calc_formula_obj(cat_data['formula'], None)
                    cat_data['parameters'] = []
                    cat_data['categories'] = self.get_form_category_data(
                        cat.categories, real_estate)
                    if cat.parameters.exists():
                        for pararmeter in cat.parameters.all():
                            formula = FormulaParameterCategory.objects.filter(
                                category=cat, parameter=pararmeter).first
                            value, rate, formula, id, result = self.get_parameter_data(
                                pararmeter, real_estate, formula)
                            pararmeter_obj = {
                                'parameter': pararmeter,
                                'formula': formula,
                                'data': {
                                    'value': value,
                                    'rate': rate,
                                    'formula': formula,
                                    'id': id,
                                    'result': result
                                }
                            }
                            cat_data['parameters'].append(pararmeter_obj)
                    data.append(cat_data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e))
            print(exc_type, fname, exc_tb.tb_lineno)
        return data

    def get(self, request):
        try:
            error = ''
            contains = []
            categories = []
            pk = int(request.GET.get('id'))
            real_property = get_object_or_404(RealEstate, id=pk)

            if real_property.search_form and real_property.search_form.categories:
                categories = real_property.search_form.categories.filter(
                    parent_categories=None)
            else:
                search_form = SearchForm.objects.get(name='default')
                categories = search_form.categories.filter(parent_categories=None)

            cat_data = self.get_form_category_data(categories, real_property)

            self.calc_rating(cat_data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(str(e))
            # print(exc_type, fname, exc_tb.tb_lineno)
            
        return render(request, self.template_name, {
            'title': 'Отчет',
            'error': error,
            'real_property': real_property,
            'data': cat_data
        })

    def calc_rating(self, category_data):
        try:
            for category in category_data:
                if len(category['categories']) == 0:
                    if category['rate'] != 0:
                        ratio = 1 if self.has_any_data(category) else 0
                        category['rate'] = ratio * category['rate']
                else:
                    self.calc_rating(category['categories'])
                    category['rate'] = calc_formula_obj(category['formula'], category['categories'])                    
        except Exception as e:
            print(e)

    def has_any_data(self, category):
        # if len(category['parameters']) == 0:
        #     return False

        # for param in category['parameters']:
        #     if param['data']['value'] == '' or \
        #         param['data']['value'] == 0:
        #         return False

        return True
