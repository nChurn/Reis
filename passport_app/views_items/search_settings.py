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
from passport_app.views_items.ajaxview import *
from passport_app.forms import *

class SearchSettingsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'passport_app.view_searchsettings',
        'passport_app.change_searchsettings',
        'passport_app.delete_searchsettings',
        'passport_app.add_searchsettings',
    )

    template_name = 'search_settings/search_settings.html'

    def get(self, request, *args, **kwargs):
        form = SearchConfigForm()

        return render(request, self.template_name,
                      {'title': 'Настройки R.E.I.S.','form': form})

    def post(self, request, *args, **kwargs):
        form = SearchConfigForm(request.POST)
        if form.is_valid():
            try:
                search_config = SearchConfig.objects.all().first()

                is_phone = request.POST.get('phone') == 'on'
                is_email = request.POST.get('email') == 'on'
                is_search_form = request.POST.get('search_form') == 'on'
                is_owner = request.POST.get('owner') == 'on'

                search_config.show_phone_field = is_phone
                search_config.show_email_field = is_email
                search_config.show_owner_field = is_owner
                search_config.show_search_form_field = is_search_form
                search_config.save()
            except Exception as e:
                print (str(e))
                pass
            return  HttpResponseRedirect('/')
        search_config = SearchConfig.objects.all().first()
        form = SearchConfigForm()
        return render(request, self.template_name,
                    {
                        'title': 'Настройки R.E.I.S.',
                        'search_config': search_config,
                        'form': form,
                    })