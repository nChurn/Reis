# from django.conf.urls import url
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
# from django.conf.urls import url
from django.urls import path
from django_select2.forms import *

from passport_app.users_funcs import *
from passport_app.views import *
from passport_app.my_views import *
from passport_app.views_items.category.category_view import *
from passport_app.views_items.details.details_view import *
from passport_app.views_items.parameter_data.parameter_data_view import *
from passport_app.views_items.parameters.parameters_view import *
from passport_app.views_items.parser.parser_parameter_view import *
from passport_app.views_items.parser.parser_type_view import *
from passport_app.views_items.property_types.subsubsubtypeofrealestate import *
from passport_app.views_items.rate_classifier.rate_classifier import *
from passport_app.views_items.search_form.search_form import *
from passport_app.views_items.search_settings import *
from passport_app.views_items.type_of_value.type_of_value_view import *
from passport_app.views_items.unit.unit_view import *

app_name = 'passport_app'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('constructor/', ConstructorView.as_view(), name="constructor"),
    
    path('constructor/constructor_container/', TConstructorContainerView.as_view()),
    path('constructor/form_container/',TFormsContainerView.as_view(),name='form_container'),
    path('constructor/parameters_container/', TParamsContainerView.as_view()),
    path('constructor/unit_container/', TUnitContainerView.as_view()),
    path('constructor/typeofvalue_container/', TTypeOfValueContainerView.as_view()),
    path('constructor/parser_container/', TParserContainerView.as_view()),
    path('constructor/category_container/', TCategoryContainerView.as_view()),
    path('constructor/get_parents_id/', TCategoryGetParentsId.as_view()),
    path('constructor/get_units_id/', TGetUnitById.as_view()),
    path('constructor/get_users_id/', TGetUserById.as_view()),
    path('constructor/get_typeofvalues_id/', TGetTypeOfValueById.as_view()),
    path('constructor/get_params_id/', TGetParameterById.as_view()),
    path('constructor/get_realstates_id/', TGetRealEstatesById.as_view()),
    #Старая логика
    # path('classifiers_list/', ClassifierView.as_view()),
    # path('fields_list/', FieldsView.as_view()),
    # path('typeofrealestates_list/', TypeOfRealEstatesView.as_view()),
    # path('subtypeofrealestates_list/', SubtypeOfRealEstatesView.as_view()),
    path('search/', SearchView.as_view()),
    path('search-archive/', SearchArchiveView.as_view()),
    path('details/edit/', EditDataFieldView.as_view()),
    path('search-archive-list/', SearchArchiveListView.as_view()),
    path('history/', HistoryView.as_view()),
    path('details/', DetailsView.as_view()),
    path('update/', DetailsUpdateView.as_view()),
    # path('region_country/<int:country_id>/', RegionListView.as_view()),
    # path('district_region/<int:region_id>/', DistrictListView.as_view()),
    # path('locality_district/<int:district_id>/<int:locality_type_id>/', LocalityListView.as_view()),
    # path('street_locality/<int:country_id>/<street_type_id>/', StreetListView.as_view()),

    # path('constructor/fields_classifier/<int:classifier_id>/', FieldListView.as_view()),
    # path('constructor/subtypes_types/<int:type_id>/', SubtypeListView.as_view()),
    # path('constructor/form_edit/', FormEditView.as_view()),
    # path('constructor/form_new/', FormNewView.as_view()),
    # path('constructor/form_view/', FormViewView.as_view()),
    # path('constructor/form_view_list/<str:name>/', SearchFormsListView.as_view()),
    # path('constructor/form_view_list/', SearchFormsListView.as_view()),
    # path('constructor/fields/', FieldsConstructorView.as_view()),
    # path('constructor/classifiers/', ClassifiersConstructorView.as_view()),
    # path('constructor/types/', TypesConstructorView.as_view()),
    # path('constructor/subtypes/', SubtypesConstructorView.as_view()),
    # path('constructor/subsubtypes/', SubsubTypesConstructorView.as_view()),
    # path('constructor/subsubtypes/add/', SubsubTypesConstructorCreate.as_view()),
    # path('constructor/subsubtypes/edit/<int:pk>/', SubsubTypesConstructorUpdate.as_view()),

    # path('constructor/subsubsubtypes/', SubsubsubTypesConstructorView.as_view()),
    # path('constructor/subsubsubtypes/add/', SubsubsubTypesConstructorCreate.as_view()),
    # path('constructor/subsubsubtypes/edit/<int:pk>/', SubsubsubTypesConstructorUpdate.as_view()),

    path('users_list/find_user/', TFormsUsersFindListView.as_view()),
    path('users_list/register/', NewUserProfileView.as_view(), name='register_user'),
    path('search_settings/', SearchSettingsView.as_view()),
    path('users_list/edit/<int:pk>/', EditUserProfileView.as_view(), name="userslist_edit"),
    path('users_list/', UsersListView.as_view(), name='userslist'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    #category
    path('constructor/categories-add/<int:category_pk>/', CategoriesAddView.as_view()),
    path('constructor/categories-delete/<int:category_pk>/<int:child_category_pk>/', CategoriesDeleteView.as_view()),
    path('constructor/category/<int:pk>/', CategoryDetails.as_view(), name='category-detail'),
    path('constructor/category-paste/', CategoryPaste.as_view()),
    path('category/add/', CategoryCreate.as_view(), name='category-add'),
    path('category/<int:pk>/', CategoryUpdate.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='category-delete'),

    path('constructor/categories/', CategoriesSearch.as_view()),
    path('constructor/categories/<int:parent>/', CategoriesParent.as_view()),
    path('categories-list/', CategoryList.as_view(), name='categories_list'),
    path('category_find/<int:pk>/', CategoryFind.as_view()),

    #parameter
    path('constructor/parameters-add/<int:category_pk>/', ParametersAddView.as_view()),
    path('constructor/parameters-remove/<int:category_pk>/<int:parameter_pk>/', ParametersRemoveView.as_view()),
    path('constructor/parameters/', ParametersSearch.as_view()),
    path('parameter/add/', ParameterCreate.as_view(), name='parameter-add'),
    path('parameter/<int:pk>/', ParameterUpdate.as_view(), name='parameter-update'),
    path('parameter/<int:pk>/delete/', ParameterDelete.as_view(), name='parameter-delete'),

    #unit
    path('constructor/units/', UnitSearch.as_view()),
    path('unit/add/', UnitCreate.as_view(), name='unit-add'),
    path('unit/<int:pk>/', UnitUpdate.as_view(), name='unit-update'),
    path('unit/<int:pk>/delete/', UnitDelete.as_view(), name='unit-delete'),

    #typeofvalue
    path('constructor/typesofvalues/', TypeOfValueSearch.as_view()),
    path('typeofvalue/add/', TypeOfValueCreate.as_view(), name='typeofvalue-add'),
    path('typeofvalue/<int:pk>/', TypeOfValueUpdate.as_view(), name='typeofvalue-update'),
    path('typeofvalue/<int:pk>/delete/', TypeOfValueDelete.as_view(), name='typeofvalue-delete'),

    #parser type
    path('constructor/parsertypes/', ParserTypeSearch.as_view()),
    path('parsertype/add/', ParserTypeCreate.as_view(), name='parser-add'),
    path('parsertype/<int:pk>/', ParserTypeUpdate.as_view(), name='parser-update'),
    path('parsertype/<int:pk>/delete/', ParserTypeDelete.as_view(), name='parser-delete'),    

    #parser parameter
    path('constructor/parserparameters/', ParserParametersSearch.as_view()),
    path('parserparameter/add/', ParserParameterCreate.as_view(), name='parser-add'),
    path('parserparameter/<int:pk>/', ParserParameterUpdate.as_view(), name='parser-update'),
    path('parserparameter/<int:pk>/delete/', ParserParameterDelete.as_view(), name='parser-delete'),
    path('constructor/parserparameters-add/<int:parser_type_pk>/', ParserParametersAddView.as_view()),
    path('constructor/parserparameters-remove/<int:parser_type_pk>/<int:parser_parameter_pk>/', ParserParametersDeleteView.as_view()),

    #forms
    path('constructor/forms/', SearchFormSearch.as_view()),
    path('forms/add/', SearchFormCreate.as_view(), name='form-add'),
    path('forms/<int:pk>/', SearchFormUpdate.as_view(), name='form-update'),
    path('forms/<int:pk>/view/', ViewFormSearch.as_view(), name='form-view'),
    path('forms/<int:pk>/delete/', SearchFormDelete.as_view(), name='form-delete'),

    #parameter data
    path('parameterdata/<int:pk>/<int:pk_d>/', ParameterDataUpdate.as_view(), name='parameterdata-update'),

    path('select2_widget', TemplateFormView.as_view(), name='select2_widget'),

    #rate classifier
    path(r'rate-classifier/', RateClassifierListView.as_view(), name='rate_classifier.list'),
    path(r'rate-classifier/create/', RateClassifierCreateView.as_view(), name='rate_classifier.create'),
    path(r'rate-classifier/<int:pk>/update/', RateClassifierUpdateView.as_view(), name='rate_classifier.update'),
    path(r'rate-classifier/<int:pk>/delete/', RateClassifierDeleteView.as_view(), name='rate_classifier.delete')
]
