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

from passport_app.api.reestr_api import (get_data_from_rosreesr_api_by_address,
                                         get_data_from_rosreesr_api_by_cn)
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

from .forms import *


class UserViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                  viewsets.ModelViewSet):
    permission_required = (
        'auth.view_user',
        'auth.change_user',
        'auth.delete_user',
        'auth.add_user',
    )
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                   viewsets.ModelViewSet):
    permission_required = (
        'auth.view_group',
        'auth.change_group',
        'auth.delete_group',
        'auth.add_group',
    )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class OwnerViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                   viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_owner',
        'passport_app.change_owner',
        'passport_app.delete_owner',
        'passport_app.add_owner',
    )
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class CountryViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                     viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_country',
        'passport_app.change_country',
        'passport_app.delete_country',
        'passport_app.add_country',
    )
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class RegionViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                    viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_region',
        'passport_app.change_region',
        'passport_app.delete_region',
        'passport_app.add_region',
    )
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DistrictViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                      viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_district',
        'passport_app.change_district',
        'passport_app.delete_district',
        'passport_app.add_district',
    )
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class TypeOfLocalityViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                            viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_typeoflocality',
        'passport_app.change_typeoflocality',
        'passport_app.delete_typeoflocality',
        'passport_app.add_typeoflocality',
    )
    queryset = TypeOfLocality.objects.all()
    serializer_class = TypeOfLocalitySerializer


class LocalityViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                      viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_locality',
        'passport_app.change_locality',
        'passport_app.delete_locality',
        'passport_app.add_locality',
    )
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer


class TypeOfStreetViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                          viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_typeofstreet',
        'passport_app.change_typeofstreet',
        'passport_app.delete_typeofstreet',
        'passport_app.add_typeofstreet',
    )
    queryset = TypeOfStreet.objects.all()
    serializer_class = TypeOfStreetSerializer


class StreetViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                    viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_street',
        'passport_app.change_street',
        'passport_app.delete_street',
        'passport_app.add_street',
    )
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class ClassifierViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                        viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_classifier',
        'passport_app.change_classifier',
        'passport_app.delete_classifier',
        'passport_app.add_classifier',
    )
    queryset = Classifier.objects.all()
    serializer_class = ClassifierSerializer


class TypeOfValueViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                         viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_typeofvalue',
        'passport_app.change_typeofvalue',
        'passport_app.delete_typeofvalue',
        'passport_app.add_typeofvalue',
    )
    queryset = TypeOfValue.objects.all()
    serializer_class = TypeOfValueSerializer


class UnitViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                  viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_unit',
        'passport_app.change_unit',
        'passport_app.delete_unit',
        'passport_app.add_unit',
    )
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class TypeOfRealEstateViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                              viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_typeofrealestate',
        'passport_app.change_typeofrealestate',
        'passport_app.delete_typeofrealestate',
        'passport_app.add_typeofrealestate',
    )
    queryset = TypeOfRealEstate.objects.all()
    serializer_class = TypeOfRealEstateSerializer


class SubtypeOfRealEstateViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                                 viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_subtypeofrealestate',
        'passport_app.change_subtypeofrealestate',
        'passport_app.delete_subtypeofrealestate',
        'passport_app.add_subtypeofrealestate',
    )
    queryset = SubtypeOfRealEstate.objects.all()
    serializer_class = SubtypeOfRealEstateSerializer


class SubsubtypeOfRealEstateViewSet(LoginRequiredMixin,
                                    PermissionRequiredMixin,
                                    viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_subsubtypeofrealestate',
        'passport_app.change_subsubtypeofrealestate',
        'passport_app.delete_subsubtypeofrealestate',
        'passport_app.add_subsubtypeofrealestate',
    )
    queryset = SubsubtypeOfRealEstate.objects.all()
    serializer_class = SubsubtypeOfRealEstateSerializer


class SubsubsubtypeOfRealEstateViewSet(LoginRequiredMixin,
                                       PermissionRequiredMixin,
                                       viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_subsubsubtypeofrealestate',
        'passport_app.change_subsubsubtypeofrealestate',
        'passport_app.delete_subsubsubtypeofrealestate',
        'passport_app.add_subsubsubtypeofrealestate',
    )
    queryset = SubsubsubtypeOfRealEstate.objects.all()
    serializer_class = SubsubsubtypeOfRealEstateSerializer


class DataFieldViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                       viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_datafield',
        'passport_app.change_datafield',
        'passport_app.delete_datafield',
        'passport_app.add_datafield',
    )
    queryset = DataField.objects.all()
    serializer_class = DataFieldSerializer


class FieldViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                   viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_field',
        'passport_app.change_field',
        'passport_app.delete_field',
        'passport_app.add_field',
    )
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class RealEstateViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                        viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_realestate',
        'passport_app.change_realestate',
        'passport_app.delete_realestate',
        'passport_app.add_realestate',
    )
    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer


class SearchFormViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                        viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_searchform',
        'passport_app.change_searchform',
        'passport_app.delete_searchform',
        'passport_app.add_searchform',
    )
    queryset = SearchForm.objects.all()
    serializer_class = SearchFormSerializer


class GroupVisitViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                        viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_groupvisit',
        'passport_app.change_groupvisit',
        'passport_app.delete_groupvisit',
        'passport_app.add_groupvisit',
    )
    queryset = GroupVisit.objects.all()
    serializer_class = GroupVisitSerializer


class UserVisitViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                       viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_uservisit',
        'passport_app.change_uservisit',
        'passport_app.delete_uservisit',
        'passport_app.add_uservisit',
    )
    queryset = UserVisit.objects.all()
    serializer_class = UserVisitSerializer


class UserUserViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                      viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_useruser',
        'passport_app.change_useruser',
        'passport_app.delete_useruser',
        'passport_app.add_useruser',
    )
    queryset = UserUser.objects.all()
    serializer_class = UserUserSerializer


class NotLoginUserVisitViewSet(LoginRequiredMixin, PermissionRequiredMixin,
                               viewsets.ModelViewSet):
    permission_required = (
        'passport_app.view_notloginuservisit',
        'passport_app.change_notloginuservisit',
        'passport_app.delete_notloginuservisit',
        'passport_app.add_notloginuservisit',
    )
    queryset = NotLoginUserVisit.objects.all()
    serializer_class = NotLoginUserVisitSerializer


# address view
class RegionListView(generics.ListAPIView):
    serializer_class = RegionSerializer

    def get_queryset(self):
        country_id = self.kwargs['country_id']
        try:
            return Region.objects.filter(country_id=country_id)
        except:
            return []


class DistrictListView(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        region_id = self.kwargs['region_id']
        try:
            return District.objects.filter(region_id=region_id)
        except:
            return []


class LocalityListView(generics.ListAPIView):
    serializer_class = LocalitySerializer

    def get_queryset(self):
        district_id = self.kwargs['district_id']
        locality_type_id = self.kwargs['locality_type_id']
        try:
            return Locality.objects.filter(
                district_id=district_id, type_of_locality_id=locality_type_id)
        except:
            return []


class StreetListView(generics.ListAPIView):
    serializer_class = StreetSerializer

    def get_queryset(self):
        district_id = self.kwargs['locality_id']
        type_street_id = self.kwargs['type_street_id']
        try:
            return Street.objects.filter(locality_id=district_id,
                                         type_of_street_id=type_street_id)
        except:
            return []


#  =====================================


class FieldListView(generics.ListAPIView):
    serializer_class = FieldSerializer

    def get_queryset(self):
        classifier_id = self.kwargs['classifier_id']
        try:
            return Field.objects.filter(classifier=classifier_id)
        except:
            return []


class SubtypeListView(generics.ListAPIView):
    serializer_class = TypeOfRealEstateSerializer

    def get_queryset(self):
        type_id = self.kwargs['type_id']
        try:
            return SubtypeOfRealEstate.objects.filter(type=type_id)
        except:
            return []


# Create your views here.


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        form = None
        forms = []
        search_config = {}
        if request.user.is_authenticated:
            current_user = request.user
            try:
                user_groups = current_user.groups.filter(name="simpleuser") | current_user.groups.filter(name="simpleadmin")
                if user_groups and user_groups.count() > 0:
                    created_user = UserUser.objects.get(
                        user_id=current_user.id)
                    forms = SearchForm.objects.filter(user_id=created_user.id)
                else:
                    forms = SearchForm.objects.filter(user_id=request.user.id)

            except Exception as e:
                pass
            form = UserSearchForm(forms=forms)
        else:
            forms = SearchForm.objects.filter(is_default=True)
            form = SimpleSearchForm()
            search_config = SearchConfig.objects.all().first()

        return render(request, self.template_name, {
            'title': '',
            'forms': forms,
            'form': form,
            'search_config': search_config
        })

class DetailsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('passport_app.change_datafield',
                           'passport_app.add_datafield')
    template_name = 'details.html'

    def get(self, request):
        real_property_id = request.GET.get('id')
        error = ''
        if not real_property_id:
            error = "id not found"
        real_property = RealEstate.objects.get(id=int(real_property_id))

        if not real_property:
            error = "real property not found"
        else:
            kadastr_number = real_property.kadastr_number
            address = real_property.address
            params = {
                'social': {},
                'transport': {},
                'place_info': {},
                'rights': {},
                'architecture': {},
                'engsys': {},
                'base': {}
            }
            get_data_from_rosreesr_api_by_cn(kadastr_number, params)
            get_data_by_address(address, params)

        # real_property_list = RealEstate.objects.filter(kadastr_number=kadastr_number)

        return render(request, self.template_name, {
            'error': error,
            'real_property': real_property
        })

    def post(self, request):
        data_fields = json.loads(request.POST.get('fields'))['data']
        new_real_property = create_new_by_old(request.user, data_fields)

        return render(request, self.template_name,
                      {'real_property': new_real_property})


class ConstructorView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'passport_app.change_classifier',
        'passport_app.change_datafield',
        'passport_app.change_field',
        'passport_app.change_subtypeofrealestate',
        'passport_app.change_realestate',
        'passport_app.change_typeofrealestate',
        'passport_app.change_searchform',
        'passport_app.add_classifier',
        'passport_app.add_datafield',
        'passport_app.add_field',
        'passport_app.add_subtypeofrealestate',
        'passport_app.add_realestate',
        'passport_app.add_typeofrealestate',
        'passport_app.add_searchform',
        'passport_app.delete_classifier',
        'passport_app.delete_datafield',
        'passport_app.delete_field',
        'passport_app.delete_subtypeofrealestate',
        'passport_app.delete_realestate',
        'passport_app.delete_typeofrealestate',
        'passport_app.delete_searchform',
    )
    template_name = 'constructor.html'

    def get(self, request):
        try:
            current_user = request.user
            categories = []  #Category.objects.filter(parent_categories = None)
            forms_list = SearchForm.objects.filter(user_id=current_user.id)
            error = ''
            category_form = CategoryForm()
            parameter_form = ParameterForm()
            parser_parameter_form = ParserParameterForm()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        return render(
            request, self.template_name, {
                'title': 'Конструктор R.E.I.S.',
                'error': error,
                'forms': forms_list,
                'categories': categories,
                'category_form': category_form,
                'parameter_form': parameter_form,
                'parser_parameter_form': parser_parameter_form
            })

    # def delete(self, request):
    #     current_user = request.user
    #     classifier_list = Classifier.objects.order_by('point')
    #     fields_list = Field.objects.order_by('classifier', 'point')
    #     types_list = TypeOfRealEstate.objects.all()
    #     subtypes_list = SubtypeOfRealEstate.objects.all()
    #     categories = Category.objects.filter(parent_categories = None)
    #     forms_list = SearchForm.objects.filter(user_id = current_user.id)
    #     error = ''
    #     category_form = CategoryForm()
    #     parameter_form = ParameterForm()
    #     return render(request, self.template_name, {'error': error, 'classifiers': classifier_list, 'fields':fields_list,
    #                                                 'types':types_list, 'subtypes':subtypes_list, 'forms':forms_list, 'categories':categories,
    #                                                 'category_form': category_form, 'parameter_form': parameter_form})


# class ClassifierView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.add_classiffier', 'passport_app.change_classifier')
#     template_name = 'classifier_view.html'

#     def get(self, request):
#         classifier_list = Classifier.objects.all()

#         error = ''
#         return render(request, self.template_name, {'error': error, 'classifiers': classifier_list})

# class TypeOfRealEstatesView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.add_typeofrealestate', 'passport_app.change_typeofrealestate')
#     template_name = 'typeofrealestate_view.html'

#     def get(self, request):
#         classifier_list = TypeOfRealEstate.objects.all()

#         error = ''
#         return render(request, self.template_name, {'error': error, 'typeofrealestates': classifier_list})

# class SubtypeOfRealEstatesView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.add_subtypeofrealestate', 'passport_app.change_subtypeofrealestate')
#     template_name = 'subtypeofrealestate_view.html'

#     def get(self, request):
#         classifier_list = SubtypeOfRealEstate.objects.all()

#         error = ''
#         return render(request, self.template_name, {'error': error, 'subtypeofrealestates': classifier_list})

# class FieldsView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.view_classifier', 'passport_app.view_country', 'passport_app.view_datafield', 'passport_app.view_district', 'passport_app.view_field', 'passport_app.view_locality', 'passport_app.view_owner', 'passport_app.view_real_estate', 'passport_app.view_region', 'passport_app.view_street', 'passport_app.view_subtypeofrealestate', 'passport_app.view_locality', 'passport_app.view_typeofrealestate', 'passport_app.view_typeofstreet', 'passport_app.view_typeofvalue', 'passport_app.view_unit')
#     template_name = 'field_view.html'

#     def get(self, request):
#         classifier_list = Field.objects.all()

#         error = ''
#         return render(request, self.template_name, {'error': error, 'fields': classifier_list})

# class FormEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.add_searchform', 'passport_app.change_searchform')
#     template_name = 'form_edit_view.html'

#     def get(self, request):
#         id = request.GET.get('id')
#         form = SearchForm.objects.get(id=id)
#         form_config = json.loads(form.config)
#         config = {'classifiers':[], 'types':[]}

#         for classifier in form_config['classifiers']:
#             try:
#                 item = {"classifier": Classifier.objects.get(id=classifier), "fields":[]}

#                 for field in form_config['classifiers'][classifier]:
#                     try:
#                         item['fields'].append(Field.objects.get(id=field))
#                     except Exception as e:
#                         pass

#                 config['classifiers'].append(item)
#             except Exception as e:
#                 pass

#         for type in form_config['types']:
#             try:
#                 item = {"type": TypeOfRealEstate.objects.get(id=type), "subtypes":[]}

#                 for subtype in form_config['types'][type]:
#                     try:
#                         item['subtypes'].append(SubtypeOfRealEstate.objects.get(id=subtype))
#                     except Exception as e:
#                         pass

#                 config['types'].append(item)
#             except Exception as e:
#                 pass

#         error = ''
#         return render(request, self.template_name, {'error': error, 'form': form, 'config':config})

# class FormNewView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.add_searchform', 'passport_app.change_searchform')
#     template_name = 'form_new_view.html'

#     def get(self, request):

#         error = ''
#         return render(request, self.template_name, {'error': error})

# class FormViewView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.add_searchform', 'passport_app.change_searchform')
#     template_name = 'form_view_view.html'

#     def get(self, request):
#         id = request.GET.get('id')
#         form = SearchForm.objects.get(id=id)
#         form_config = json.loads(form.config)
#         config = {'classifiers':[], 'types':[]}
#         for classifier in form_config['classifiers']:
#             try:
#                 item = {"classifier": Classifier.objects.get(id=classifier), "fields":[]}

#                 for field in form_config['classifiers'][classifier]:
#                     try:
#                         item['fields'].append(Field.objects.get(id=field))
#                     except Exception as e:
#                         pass

#                 config['classifiers'].append(item)
#             except Exception as e:
#                 pass

#         for type in form_config['types']:
#             try:
#                 item = {"type": TypeOfRealEstate.objects.get(id=type), "subtypes":[]}

#                 for subtype in form_config['types'][type]:
#                     try:
#                         item['subtypes'].append(SubtypeOfRealEstate.objects.get(id=subtype))
#                     except Exception as e:
#                         pass

#                 config['types'].append(item)
#             except Exception as e:
#                 pass

#         error = ''
#         return render(request, self.template_name, {'error': error, 'form': form, 'config':config})


class SearchView(FormView):
    template_name = 'index.html'
    form_class = UserSearchForm
    success_url = '/'

    def form_valid(self, form):
        search_history = []
        current_user = None
        if self.request.user.is_authenticated:
            current_user = self.request.user

        search_param = form['kadastr_number'].value()
        email = None
        search_form = None
        kadastr_number = ''

        try:
            search_form = form['search_form'].value()

            if search_form is None:
                search_form = SearchForm.objects.filter(name="default").first().id
        except Exception as e:
            pass
        params = create_property_dict()

        try:
            match = re.search("\d{1,3}\:\d{1,3}\:\d{1,8}\:\d{1,7}", search_param)  # Get all IPs line by line
            base_address = ""
            params['base'] = {}
            kadastr_number = search_param

            if match:
                get_data_from_rosreesr_api_by_cn(search_param, params)
                address = params['base']['address']
            else:
                address = search_param

            base_address = yandex_get_address_data(address)

            logger.error('base address')
            logger.error(base_address['point'])
            logger.error(base_address['text_address'])
            
            owner = Owner()

            match = re.search("\d{12}", form['owner'].value())
            if not match:
                owner.name = form['owner'].value()
            else:
                owner.inn = form['owner'].value()
            owner.save()

            real_estate = RealEstate()
            real_estate.report_number = RealEstate.objects.all().count() + 1
            real_estate.owner = owner
            real_estate.user = current_user
            real_estate.search_form_id = search_form

            real_estate.country_name = base_address['country']
            real_estate.region_name = base_address['province']
            real_estate.district_name = base_address['province2']
            real_estate.locality_name = base_address['locality']
            real_estate.street_name = base_address['street']
            real_estate.house_number = base_address['house']
            real_estate.address = base_address['text_address']

            pos = base_address['point'].split(' ')
            real_estate.latitude = pos[1]
            real_estate.longitude = pos[0]

            real_estate.save()

            #start_search_info(real_estate.address, real_estate)

            launcher = DataSourcesLauncher(real_estate)
            launcher.start_parsing()
            
            search_history = RealEstate.objects.filter(user=current_user, 
                address=real_estate.address).values('address').order_by('address').annotate(count=Count('address'))
        except Exception as e:
            PrintException()

        print("send email")
        if email:
            send_search_result(params, email, kadastr_number)
            messages.add_message(request, messages.INFO,
                                 'Результат поиска отправлен на почту')

            # return HttpResponseRedirect('/', {'form':form})
            # html = render_to_string('partial_history_view.html', {'data': []}, request=request)

        print("render history")
        html = render_to_string('partial_history_view.html',
                                {'data': search_history},
                                request=self.request)
        return HttpResponse(html)

        # return super().form_valid(form)


class SearchArchiveView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'passport_app.view_classifier', 'passport_app.view_country',
        'passport_app.view_datafield', 'passport_app.view_district',
        'passport_app.view_field', 'passport_app.view_locality',
        'passport_app.view_owner', 'passport_app.view_real_estate',
        'passport_app.view_region', 'passport_app.view_street',
        'passport_app.view_subtypeofrealestate', 'passport_app.view_locality',
        'passport_app.view_typeofrealestate', 'passport_app.view_typeofstreet',
        'passport_app.view_typeofvalue', 'passport_app.view_unit')

    def post(self, request, *args, **kwargs):
        current_user = request.user
        kadastr_number = request.POST.get('kadastr_number')
        print(kadastr_number)
        search_history = []
        search_str = "%" + kadastr_number + "%"
        form = UserSearchForm(request.POST)
        # if form.is_valid():
        #     print(form.errors)
        #     form = UserSearchForm()
        #     print ("redirect home")
        #     return  HttpResponseRedirect('/', {'form':form})

        search_form = None
        try:
            search_form = int(request.POST.get('search_form'))
        except Exception as e:
            pass

        if search_form and search_form == -1:
            search_form = None

        error = ''
        result = None
        match = re.search("\d{1,3}\:\d{1,3}\:\d{1,8}\:\d{1,7}",
                          kadastr_number)  # Get all IPs line by line
        if match:
            if kadastr_number:
                print("kadastr_number search")
                print(search_form)
                if not search_form:
                    search_history = RealEstate.objects.filter(
                        user=current_user,
                        kadastr_number__contains=kadastr_number).values(
                            'address',
                            'kadastr_number').order_by('address').annotate(
                                count=Count('address'))
                else:
                    search_history = RealEstate.objects.filter(
                        user=current_user,
                        kadastr_number__contains=kadastr_number,
                        search_form=search_form).values(
                            'address',
                            'kadastr_number').order_by('address').annotate(
                                count=Count('address'))
            else:
                error = "kadastr number not found"

            # if not result:
            if not result:
                error = "kadastr number not found"

        else:
            print("address search")
            print(search_form)
            print(current_user.id)
            if not search_form:
                search_history = RealEstate.objects.filter(
                    user=current_user,
                    address__contains=kadastr_number).values(
                        'address',
                        'kadastr_number').order_by('address').annotate(
                            count=Count('address'))
            else:
                search_history = RealEstate.objects.filter(
                    user=current_user,
                    address__contains=kadastr_number,
                    search_form=search_form).values(
                        'address',
                        'kadastr_number').order_by('address').annotate(
                            count=Count('address'))

        print("render history")
        print(search_history.count())
        html = render_to_string('partial_history_view.html',
                                {'data': search_history},
                                request=request)
        return HttpResponse(html)
        # return HttpResponseRedirect('/', {'form':form})


class SearchArchiveListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'passport_app.view_classifier', 'passport_app.view_country',
        'passport_app.view_datafield', 'passport_app.view_district',
        'passport_app.view_field', 'passport_app.view_owner',
        'passport_app.view_region', 'passport_app.view_street',
        'passport_app.view_subtypeofrealestate', 'passport_app.view_locality',
        'passport_app.view_realestate', 'passport_app.view_typeofrealestate',
        'passport_app.view_typeofstreet', 'passport_app.view_typeofvalue',
        'passport_app.view_unit')

    def post(self, request, *args, **kwargs):
        error = ''
        result = None
        real_property_list = []
        qs_json = ''
        kadastr_number = None
        try:
            current_user = request.user
            kadastr_number = request.POST.get('kadastr_number_archive')
            print(kadastr_number)
            match = re.search("\d{1,3}\:\d{1,3}\:\d{1,8}\:\d{1,7}",
                              kadastr_number)
            if match:
                # if kadastr_number:
                #     result = RealEstate.objects.filter(user=current_user, kadastr_number = kadastr_number)
                # else:
                #     error = "kadastr number not found"

                # # if not result:
                # if not result:
                #     error = "kadastr number not found"

                real_property_list = RealEstate.objects.filter(
                    user=current_user, kadastr_number=kadastr_number)
            else:
                # result = RealEstate.objects.filter(address=kadastr_number)
                # # if not result:
                # if not result.exists():
                #     error = "kadastr number not found"

                real_property_list = RealEstate.objects.filter(
                    user=current_user, address__contains=kadastr_number
                )  #(user=current_user, address=kadastr_number)
            if not real_property_list.exists():
                real_property_list = []
            qs_json = serializers.serialize('json', real_property_list)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            real_property_list = []
            qs_json = serializers.serialize('json', real_property_list)

        return JsonResponse({
            'error': error,
            'kadastr_number': kadastr_number,
            'real_property_list': qs_json
        })


class HistoryView(View):
    def get(self, request):
        current_user = request.user

        search_history = []
        if current_user.is_authenticated:
            search_history = RealEstate.objects.filter(
                user=current_user).values(
                    'address', 'kadastr_number').order_by('address').annotate(
                        count=Count('address'))

        html = render_to_string('partial_history_view.html',
                                {'data': search_history},
                                request=request)
        return HttpResponse(html)


class EditDataFieldView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'passport_app.view_classifier',
        'passport_app.view_country',
        'passport_app.view_datafield',
        'passport_app.view_district',
        'passport_app.view_field',
        'passport_app.view_owner',
        'passport_app.view_region',
        'passport_app.view_street',
        'passport_app.view_subtypeofrealestate',
        'passport_app.view_locality',
        'passport_app.view_realestate',
        'passport_app.view_typeofrealestate',
        'passport_app.view_typeofstreet',
        'passport_app.view_typeofvalue',
        'passport_app.view_unit',
        'passport_app.change_datafield',
    )

    def post(self, request, *args, **kwargs):

        field_id = int(request.POST.get('modal-field-id'))
        field_value = request.POST.get('modal-field-value')
        field_rate = request.POST.get('modal-field-rate')

        data_field = None
        error = ''
        if field_id:
            data_field = DataField.objects.get(id=field_id)
            if data_field:
                try:
                    data_field.value = field_value
                    data_field.rate = float(field_rate)
                    # data_field.save()
                    serializer = DataFieldSerializer(data_field)
                    if serializer.is_valid():
                        serializer.update()
                        messages.add_message(request, messages.INFO, 'updated')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, e)

        else:
            messages.add_message(request, messages.ERROR, 'field not found')

        return JsonResponse({
            'error': error,
            'data_field_val': data_field.value,
            'data_field_rate': data_field.rate,
            'data_field_id': data_field.id
        })


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('auth.add_user', 'auth.view_user')
    template_name = 'users_view.html'

    def get(self, request, *args, **kwargs):
        current_user = None
        groups = request.user.groups.all()
        user_serializer = []
        group_serializer = {}
        visits = {}
        serializer_context = {
            'request': Request(request),
        }

        search_query = request.GET.get('q', None)
        print(search_query)

        if request.user:
            current_user = request.user

        if current_user:
            if groups and groups.count() > 0 and groups[0].name == "SystemAdministrator":
                users_ids = UserUser.objects.values('user_id').filter(
                    creator_user_id=current_user.id)
                user_serializer = User.objects.filter(id__in=users_ids)
                group_serializer = Group.objects.filter(
                    name__in=['Administrator', 'SimpleUser'])
                visits = {}
            else:
                user_serializer = User.objects.all()
                group_serializer = Group.objects.all()
                visits = GroupVisit.objects.all()

        if search_query:
            user_serializer = user_serializer.filter(username__icontains=search_query,
                first_name__icontains=search_query, last_name__icontains=search_query)

        form = UserProfileForm(groups=group_serializer)
        return render(request, self.template_name, {
                'title': 'Пользователи R.E.I.S.',
                'query': search_query,
                'users': user_serializer,
                'groups': group_serializer,
                'visits': visits,
                'form': form
            })


# class FieldsConstructorView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.change_classifier',
#                            'passport_app.change_datafield',
#                            'passport_app.change_field',

#                            'passport_app.add_classifier',
#                            'passport_app.add_datafield',
#                            'passport_app.add_field',

#                            'passport_app.delete_classifier',
#                            'passport_app.delete_datafield',
#                            'passport_app.delete_field',
#                           )

#     def get(self, request, *args, **kwargs):
#         fields = Field.objects.order_by('classifier', 'point')

#         html = render_to_string('field_view.html', {'fields': fields}, request=request)
#         return HttpResponse(html)

# class ClassifiersConstructorView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.change_classifier',
#                            'passport_app.add_classifier',
#                            'passport_app.delete_classifier',
#                           )

#     def get(self, request, *args, **kwargs):
#         classifiers = Classifier.objects.order_by('point')

#         html = render_to_string('classifier_view.html', {'classifiers': classifiers}, request=request)
#         return HttpResponse(html)

# class TypesConstructorView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.change_typeofrealestate',
#                            'passport_app.add_typeofrealestate',
#                            'passport_app.delete_typeofrealestate',
#                           )

#     def get(self, request, *args, **kwargs):
#         types = TypeOfRealEstate.objects.all()

#         html = render_to_string('typeofrealestate_view.html', {'types': types}, request=request)
#         return HttpResponse(html)

# class SubsubTypesConstructorView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.change_subsubtypeofrealestate',
#                            'passport_app.add_subsubtypeofrealestate',
#                            'passport_app.delete_subsubtypeofrealestate',
#                            )

#     def get(self, request, *args, **kwargs):
#         types = SubsubtypeOfRealEstate.objects.all()
#         form = SubsubtypeOfRealEstateForm()
#         html = render_to_string('subsubtype/subsubtype_view.html', {'subsubtypes': types, 'form': form}, request=request)
#         return HttpResponse(html)

# class SubsubTypesConstructorCreate(LoginRequiredMixin, CreateView):
#     model = SubsubtypeOfRealEstate
#     fields = ['name', 'title_rus', 'title', 'subtype']
#     success_url = '/constructor/'
#     # success_message = "saved."

# class SubsubTypesConstructorUpdate(LoginRequiredMixin, SuccessMessageMixin, AjaxTemplateMixin, UpdateView):
#     template_name = 'subsubtype/partial_modal_edit_subsubttype.html'
#     model = SubsubtypeOfRealEstate
#     fields = ['name', 'title_rus', 'title', 'subtype']
#     success_url = '/constructor/'
#     success_message = "Changes saved."

# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class SubtypesConstructorView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('passport_app.change_subtypeofrealestate',
#                            'passport_app.add_subtypeofrealestate',
#                            'passport_app.delete_subtypeofrealestate',
#                           )

#     def get(self, request, *args, **kwargs):
#         subtypes = SubtypeOfRealEstate.objects.all()

#         html = render_to_string('subtypeofrealestate_view.html', {'subtypes': subtypes}, request=request)
#         return HttpResponse(html)


class NewUserProfileView(LoginRequiredMixin, FormView):
    template_name = "users_view.html"
    form_class = UserProfileForm
    success_url = '/users_list/'

    # success_url = reverse_lazy('userslist')

    def form_valid(self, form):

        user = form.save()
        user_user = UserUser()
        user_user.creator_user = self.request.user
        user_user.user = user
        user_user.save()

        return super(NewUserProfileView, self).form_valid(form)


class EditUserProfileView(
        UpdateView):  #Note that we are using UpdateView and not FormView
    # permission_required = ('auth.change_user'
    #                        )
    model = User
    form_class = UserProfileForm
    success_url = '/users_list/'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user


# class SearchFormsListView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = (
#         'passport_app.view_searchform',
#         'passport_app.change_searchform',
#         'passport_app.delete_searchform',
#         'passport_app.add_searchform',
#                            )

#     def get(self, request, *args, **kwargs):
#         form_name = None

#         try:
#             form_name = self.kwargs['name']
#         except:
#             pass
#         if not form_name:
#             forms = SearchForm.objects.all()
#         else:
#             forms = SearchForm.objects.filter(name__contains = form_name)
#         html = render_to_string('form_list.html', {'forms': forms}, request=request)
#         return HttpResponse(html)
