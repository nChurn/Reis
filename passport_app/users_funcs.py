import json
import os
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
from passport_app.email_manager import send_search_result
from passport_app.models import *
from passport_app.parser.parser_ru import get_data_by_address
from passport_app.print_exception import *
from passport_app.real_estate_manager import (create_new_by_old,
                                              create_new_real_estate,
                                              create_property_dict,
                                              update_real_estate)
from passport_app.serializers import *
from passport_app.views_helpers import *
from passport_app.views_items.ajaxview import *
from passport_app.views_items.category import *
from passport_app.views_items.parameters import *
from passport_app.views_items.property_types.subsubsubtypeofrealestate import *
from passport_app.views_items.search_settings import *
from passport_app.views_items.unit import *

from .forms import *


# Функционал поиска пользователей
#Прокси-объект для преобразования users
class UserProxy:
    def __init__(self):
        self.id=-1
        self.name=''
        self.name_ru=''

def ConvertUsersToProxy():
    users_list = User.objects.all()
    list_proxy=list()
    for item in users_list:
        obj_=UserProxy()
        obj_.id=item.id
        obj_.name=item.username+' '+item.first_name+' '+item.last_name
        obj_.name_ru=item.email
        list_proxy.append(obj_)
    return  list_proxy
def GetUserFromProxy(proxy_):
    user_=User.objects.get(id=proxy_.id)
    return user_
#
class TFormsUsersFindListView(LoginRequiredMixin, FormView):
    permission_required = ('auth.view_user')
    template_name = 'users_view_table.html'
    def get(self, request, *args, **kwargs):
        proxy_list=ConvertUsersToProxy()
        input_ = request.GET['input_str']
        # Алгоритм горизонтального поиска по справочнику
        users_helper = HorizontalSearchHelper()
        users_helper.Model = proxy_list
        users_helper.input_str = input_
        # Получение прокси-объектов
        users_proxy = users_helper.Run()
        print(users_proxy)
        res_=list()
        #Цикл по прокси
        for item in users_proxy:
            #Извлечение объекта-оригинала из БД
            user_=GetUserFromProxy(item.item)
            name_=item.name.strip()
            vals=name_.split()
            user_.username=vals[0]
            user_.first_name=vals[1]
            user_.last_name=vals[2]
            user_.email=item.name_ru
            res_.append(user_)
        #Веб-функционал
        current_user = None
        groups = request.user.groups.all()
        user_serializer = []
        group_serializer = {}
        visits = {}
        serializer_context = {
            'request': Request(request),
        }
        if request.user:
            current_user = request.user
        if current_user:
            if groups and groups.count() > 0 and groups[0].name == "SystemAdministrator":
                group_serializer = Group.objects.filter(name__in=['Administrator', 'SimpleUser'])
                visits = {}
            else:
                group_serializer = Group.objects.all()
                visits = GroupVisit.objects.all()
        form = UserProfileForm(groups=group_serializer)
        return render(request, self.template_name,
                      {'users': res_})

class TGetUserById(LoginRequiredMixin, FormView):
    permission_required = ('auth.view_user')
    template_name = 'users_view_table.html'
    def get(self, request, *args, **kwargs):
        id_ = request.GET['id']
        print(id_)
        #id_ = int(id_)
        user_ = User.objects.filter(id=id_)
        # Веб-функционал
        current_user = None
        groups = request.user.groups.all()
        user_serializer = []
        group_serializer = {}
        visits = {}
        serializer_context = {
            'request': Request(request),
        }
        if request.user:
            current_user = request.user
        if current_user:
            if groups and groups.count() > 0 and groups[0].name == "SystemAdministrator":
                group_serializer = Group.objects.filter(name__in=['Administrator', 'SimpleUser'])
                visits = {}
            else:
                group_serializer = Group.objects.all()
                visits = GroupVisit.objects.all()
        form = UserProfileForm(groups=group_serializer)
        return render(request, self.template_name,
                      {'users': user_})

