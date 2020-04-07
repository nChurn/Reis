from django.shortcuts import render
from django.views import View
from passport_app.api.reestr_api import get_data_from_rosreesr_api_by_address, get_data_from_rosreesr_api_by_cn
from passport_app.parser.parser_ru import get_data_by_address

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from passport_app.serializers import *
from passport_app.real_estate_manager import update_real_estate, create_new_real_estate, create_property_dict
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
from passport_app.forms import *
from passport_app.views_items.ajaxview import *

class SubsubsubTypesConstructorView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('passport_app.change_subsubsubtypeofrealestate',
                           'passport_app.add_subsubsubtypeofrealestate',
                           'passport_app.delete_subsubsubtypeofrealestate',
                           )

    def get(self, request, *args, **kwargs):
        types = SubsubsubtypeOfRealEstate.objects.all()
        form = SubsubsubtypeOfRealEstateForm()
        html = render_to_string('subsubsubtype/subsubtype_view.html', {'subsubsubtypes': types, 'form': form}, request=request)
        return HttpResponse(html)

class SubsubsubTypesConstructorCreate(LoginRequiredMixin, CreateView):
    model = SubsubsubtypeOfRealEstate
    fields = ['name', 'title_rus', 'title', 'subsubtype']
    success_url = '/constructor/'
    # success_message = "saved."

class SubsubsubTypesConstructorUpdate(LoginRequiredMixin, SuccessMessageMixin, AjaxTemplateMixin, UpdateView):
    template_name = 'subsubsubtype/partial_modal_edit_subsubtype.html'
    model = SubsubsubtypeOfRealEstate
    fields = ['name', 'title_rus', 'title', 'subsubtype']
    success_url = '/constructor/'
    success_message = "Changes saved."