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

class RealEstate_Proxy:
    def __init__(self):
        self.id=-1
        self.name=''
        self.name_ru=''

def ConvertRealEstateToProxy():
    RealEstate_list = RealEstate.objects.all().values('address', 'kadastr_number','id').order_by('address').annotate(count=Count('address'))
    list_proxy=list()
    for item in RealEstate_list:
        print(item)
        obj_=RealEstate_Proxy()
        obj_.id=item['id']
        obj_.name=item['address']+'_'+str(item['count'])
        obj_.name_ru=item['kadastr_number']
        list_proxy.append(obj_)
    return  list_proxy

def GetRealEstateFromProxy(proxy_):
    obj_=RealEstate.objects.get(id=proxy_.id)
    return obj_

class TGetRealEstatesById(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        id_ = request.GET['id']
        obj_ = RealEstate.objects.get(id=id_)
        print(obj_.address)
        data={'kadastr_':obj_.address}
        print(data)
        #return JsonResponse(request, "constructor_form.html", context=data)
        return JsonResponse(data)
        #return render(request,"constructor_form.html",context=data)
