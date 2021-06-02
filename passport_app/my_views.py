
from django.shortcuts import render
from django.views import View
from passport_app.api.reestr_api import get_data_from_rosreesr_api_by_address, get_data_from_rosreesr_api_by_cn
from passport_app.parser.parser_ru import get_data_by_address

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from passport_app.serializers import *
from passport_app.real_estate_manager import update_real_estate, create_new_real_estate, create_property_dict, create_new_by_old
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import generics
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.template.loader import render_to_string
import re
import json
from django.db.models import Count
from django.db.models import Value
from django.http import HttpResponse
from rest_framework import permissions
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from passport_app.email_manager import send_search_result
from rest_framework.request import Request
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from passport_app.api.ru.yandexmaps_api import *
from django.urls import reverse
from django.views.generic import *
from django.urls import reverse_lazy
from django.shortcuts import *
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
from passport_app.views_items.ajaxview import *
from passport_app.views_items.search_settings import *
from passport_app.views_items.property_types.subsubsubtypeofrealestate import *
from passport_app.views_items.category import *
from passport_app.views_items.parameters import *
from passport_app.views_items.unit import *
from passport_app.models import *
import sys, os
from passport_app.data_sources.data_sources_manager import start_search_info
from passport_app.print_exception import *
from passport_app.RealEstate_funcs import *
from passport_app.users_funcs import *


#Классы поиска по формам
class TConstructorContainerView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):

        #Список хелперов
        list_helpers=[]
        input_ = request.GET['input_str']
        categories_helper = TreeSearchHelper()
        categories_helper.Model = Category
        categories_helper.input_str = input_
        categories_helper.Name='Справочник среднего уровня'
        categories_helper.Decorator=CategoryFormDecorator()
        list_helpers.append(categories_helper)
        #
        units_helper = HorizontalSearchHelper()
        units_helper.Model = Unit
        units_helper.input_str = input_
        units_helper.Name='Единицы измерения'
        units_helper.Decorator=UnitFormDecorator()
        list_helpers.append(units_helper)
        #
        parser_helper = HorizontalSearchHelper()
        parser_helper.Model = ParserType
        parser_helper.input_str = input_
        parser_helper.Name = 'Параметры парсера'
        parser_helper.Decorator=ParserFormDecorator()
        list_helpers.append(parser_helper)
        #
        type_of_values_helper = HorizontalSearchHelper()
        type_of_values_helper.Model = TypeOfValue
        type_of_values_helper.input_str = input_
        type_of_values_helper.Name = 'Типы значений'
        type_of_values_helper.Decorator=TypeOfValueFormDecorator()
        list_helpers.append(type_of_values_helper)
        #
        parameters_helper = HorizontalSearchHelper()
        parameters_helper.Model = Parameter
        parameters_helper.input_str = input_
        parameters_helper.Decorator=ParametersFormDecorator()
        parameters_helper.Name='Справочник нижнего уровня'
        list_helpers.append(parameters_helper)
        #
        forms_helper = HorizontalSearchHelper()
        forms_helper.Model = SearchForm
        forms_helper.input_str = input_
        forms_helper.Decorator=LinkFormDecorator()
        forms_helper.Name = 'Справочник верхнего уровня'
        list_helpers.append(forms_helper)
        #
        proxy_list = ConvertUsersToProxy()
        input_ = request.GET['input_str']
        # Алгоритм горизонтального поиска по справочнику
        users_helper = HorizontalSearchHelper()
        users_helper.Model = proxy_list
        users_helper.Decorator=UserFormDecorator()
        users_helper.input_str = input_
        users_helper.Name = 'Пользователи'
        # Получение прокси-объектов
        list_helpers.append(users_helper)
        #
        proxy_list = ConvertRealEstateToProxy()
        input_ = request.GET['input_str']
        # Алгоритм горизонтального поиска по справочнику
        realestate_helper = HorizontalSearchHelper()
        realestate_helper.Model = proxy_list
        realestate_helper.Decorator = RealEstateFormDecorator()
        realestate_helper.input_str = input_
        realestate_helper.Name = 'Поиск по архиву'
        # Получение прокси-объектов
        list_helpers.append(realestate_helper)
        #
        list_results=[]
        print(list_helpers)
        for item in list_helpers:
            item.IsMaster=False
            list_=item.ConvertResult()
            print(item.Name,'!-!',list_)
            for item_ in list_:
                list_results.append(item_)
        print(list_results)
        html = render_to_string('constructor_form.html',
                                 {'list_results': list_results}, request=request)
        #html=''
        return HttpResponse(html)



class TCategoryContainerView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        categories=[]
        input_ = request.GET['input_str']
        form = CategoryForm()
        # Алгоритм вертикального поиска по справочнику среднего уровня
        categories_helper = TreeSearchHelper()
        categories_helper.Model = Category
        categories_helper.input_str = input_
        res_ = categories_helper.RunAll()
        print('<>0',res_)
        for item in res_:
            print(item.name_ru)
        html = render_to_string('category/category_container.html',
                                {'categories': res_}, request=request)
        return HttpResponse(html)
# Поиск по критериям для случая формы единиц измерения
class TUnitContainerView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        input_ = request.GET['input_str']
        units_helper = HorizontalSearchHelper()
        units_helper.Model = Unit
        units_helper.input_str = input_
        units = units_helper.Run()
        form = UnitForm()
        html = render_to_string('unit/unit_container.html', {'units': units, 'unit_form': form}, request=request)
        return HttpResponse(html)

# Поиск по критериям для случая формы парсеров
class TParserContainerView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        # from django.db.models import Q
        # parser_type_name = None
        # parser_types = []
        # name_ = request.GET['name']
        # name_ru = request.GET['name_ru']
        # if name_ru != '':
        #     parser_types = ParserType.objects.filter(name=name_, name_ru=name_ru)
        # else:
        #     parser_types = ParserType.objects.filter(Q(name=name_)|Q(name_ru=name_))
        #
        input_ = request.GET['input_str']
        parser_helper = HorizontalSearchHelper()
        parser_helper.Model = ParserType
        parser_helper.input_str = input_
        parser_types = parser_helper.Run()
        form = ParserTypeForm()
        parser_parameter_form = ParserParameterForm()
        parser_parameters = ParserParameter.objects.all()
        #parser_parameters = ParserParameter.objects.filter(parser_type=str(parser_types[0]))
        #html = render_to_string('parser/parser_container.html', {'parser_types': parser_types, 'parser_type_form': form,
         #                                                        'parser_parameter_form': parser_parameter_form,
         #                                                        'parser_parameters': parser_parameters},
                                #request=request)
        html = render_to_string('parser/parser_container.html', {'parser_types': parser_types,'parser_type_form': form,'parser_parameter_form': parser_parameter_form,'parser_parameters': parser_parameters},
         request=request)
        return HttpResponse(html)
# Поиск по критериям для случая формы типов значений
class TTypeOfValueContainerView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        input_ = request.GET['input_str']
        #Алгоритм горизонтального поиска по типам значений
        type_of_values_helper = HorizontalSearchHelper()
        type_of_values_helper.Model = TypeOfValue
        type_of_values_helper.input_str = input_
        type_of_values = type_of_values_helper.Run()
        form = TypeOfValueForm()
        html = render_to_string('type_of_value/typeofvalue_container.html',
                                {'type_of_values': type_of_values, 'type_of_value_form': form}, request=request)
        return HttpResponse(html)


# Поиск по критериям для случая формы нижнего уровня
class TParamsContainerView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        input_ = request.GET['input_str']
        # Алгоритм горизонтального поиска по справочнику нижнего уровня
        parameters_helper = HorizontalSearchHelper()
        parameters_helper.Model = Parameter
        parameters_helper.input_str = input_
        parameters = parameters_helper.Run()
        print('!',parameters)
        form = ParameterForm()
        html = render_to_string('parameter/parameter_container.html',
                                {'parameters': parameters}, request=request)
        return HttpResponse(html)

from passport_app.views_helpers import *
# Поиск по критериям для случая формы
class TFormsContainerView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        #from common_funcs import *
        input_ = request.GET['input_str']
        # Алгоритм горизонтального поиска по справочнику верхнего уровня
        forms_helper=HorizontalSearchHelper()
        forms_helper.Model=SearchForm
        forms_helper.input_str=input_
        res_=forms_helper.Run()
        form = FormSearchForm(user=request.user)
        categories = Category.objects.filter(parent_categories=None)
        html = render_to_string('search_form/form_container.html',
                                {'search_forms': res_, 'form': form, 'categories': categories,
                                 'form_categories': []}, request=request)
        return HttpResponse(html)
#  Сервисные контроллеры
class TCategoryGetParentsId(LoginRequiredMixin, FormView):
    template_name='category/category_container.html'
    def get(self, request, *args, **kwargs):
        tree_helper=TreeSearchHelper()
        tree_helper.Model=Category
        id_=request.GET['id']
        id_=int(id_)
        parents=tree_helper.GetParentsFromId(id_)
        print(parents)
        list_=list()
        index=0
        for item in parents:
            if index==0:
                list_.append(item.item.id)
            else:
                list_.append(item.id)
            index+=1
        print(list_)
        context={'list_' : str(list_)}
        return HttpResponse(str(list_))

class TGetUnitById(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        form = UnitForm()
        units=[]
        id_ = request.GET['id']
        print(id_)
        #id_ = int(id_)
        units=Unit.objects.filter(id=id_)
        html = render_to_string('unit/unit_container.html', {'units': units, 'unit_form': form}, request=request)
        return HttpResponse(html)

class TGetTypeOfValueById(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        id_ = request.GET['id']
        type_of_values=TypeOfValue.objects.filter(id=id_)
        form = TypeOfValueForm()
        html = render_to_string('type_of_value/typeofvalue_container.html',
                                {'type_of_values': type_of_values, 'type_of_value_form': form}, request=request)
        return HttpResponse(html)
class TGetParameterById(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        id_ = request.GET['id']
        form = ParameterForm()
        parameters=Parameter.objects.filter(id=id_)
        print(parameters)
        html = render_to_string('parameter/parameter_container.html',
                                {'parameters': parameters, 'parameter_form': form}, request=request)
        return HttpResponse(html)