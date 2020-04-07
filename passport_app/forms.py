from django import forms
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from passport_app.models import *
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group
from passport_app.forms_fields.subtype_model_choice_field import *
from passport_app.forms_fields.subsubtype_model_choice_field import *
from passport_app.forms_fields.form_model_choice_field import *
from passport_app.forms_fields.category_model_choice_field import *
from passport_app.models import *
from passport_app.tree_widget import *
from django_select2.forms import *
from passport_app.widgets import *


def clean_unique(form,
                 field,
                 exclude_initial=True,
                 format="The %(field)s %(value)s has already been taken."):
    value = form.cleaned_data.get(field)
    if value:
        qs = form._meta.model._default_manager.filter(**{field: value})
        if exclude_initial and form.initial:
            initial_value = form.initial.get(field)
            qs = qs.exclude(**{field: initial_value})
        if qs.count() > 0:
            raise forms.ValidationError(format % {
                'field': field,
                'value': value
            })
    return value


class SimpleSearchForm(forms.Form):
    email = forms.EmailField(
        label='Почта',
        required=False,
        help_text=
        'Укажите свой электронный адрес, куда придет сформированный отчёт')

    phone = forms.CharField(
        label='Телефон',
        max_length=10,
        validators=[
            RegexValidator(r'^\d+$', 'Enter a valid phone number.'),
        ],
        required=False,
        error_messages={'incomplete': 'Enter a valid phone number.'},
        help_text=
        'Укажите свой телефонный номер, куда придет подтверждение о формировании  отчёта'
    )

    owner = forms.CharField(
        label='Данные собственника объекта недвижимости',
        max_length=255,
        required=False,
        error_messages={
            'required':
            'Укажите наименование собственника объекта недвижимости'
        },
        help_text='Укажите ФИО или ИНН собственника объекта недвижимости')

    search_form = forms.ChoiceField(
        label='Форма',
        required=False,
        help_text='Выберите форму в зависимости от объекта недвижимости')

    kadastr_number = forms.CharField(
        label='Адрес объекта или кадастровый номер',
        max_length=255,
        error_messages={
            'required': 'Укажите адрес объекта или кадастровый номер'
        })

    captcha = CaptchaField(help_text='Введите текст с изображения слева')

    def __init__(self, *args, **kwargs):
        super(SimpleSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-9 pt-3'

        choices = [(pt.id, pt.name_ru)
                   for pt in SearchForm.objects.filter(is_default=True)]
        self.fields['search_form'].choices = choices


class UserSearchForm(forms.Form):
    search_form = SearchFormModelChoiceField(
        label='Форма',
        queryset=SearchForm.objects.all(),
        empty_label="Все",
        required=False,
        help_text='Выберите форму в зависимости от объекта недвижимости')

    kadastr_number = forms.CharField(
        label='Адрес объекта или кадастровый номер',
        max_length=255,
        error_messages={
            'required': 'Укажите адрес объекта или кадастровый номер'
        })

    owner = forms.CharField(
        label='Наименование собственника объекта недвижимости',
        max_length=255,
        required=False,
        error_messages={
            'required':
            'Укажите наименование собственника объекта недвижимости'
        })

    def __init__(self, *args, **kwargs):
        user_forms = kwargs.pop('forms', None)
        super(UserSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10 pt-3'

        # choices = [(pt.id, pt.name_ru) for pt in user_forms]
        self.fields['search_form'].initial = user_forms


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        groups_query = kwargs.pop('groups', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        try:
            if groups_query:
                self.fields['groups'].queryset = groups_query
        except:
            pass

        self.fields['email'].help_text = 'Введите свой электронный адрес'
        self.fields['password'].help_text = 'Введите пароль для пользователя'
        self.fields['first_name'].help_text = 'Введите имя пользователя'
        self.fields['last_name'].help_text = 'Введите имя пользователя'
        self.fields['first_name'].help_text = 'Введите фамилию пользователя'

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'groups')  #Note that we didn't mention user field here.


class SubsubtypeOfRealEstateForm(forms.ModelForm):
    subtype = SubtypeModelChoiceField(
        queryset=SubtypeOfRealEstate.objects.all(),
        label="Подкатегория недвижимости")

    class Meta:
        model = SubsubtypeOfRealEstate
        fields = ('name', 'title_rus', 'title', 'subtype')
        labels = {
            "name": "Название(en)",
            "title_rus": "Заголовок(ру)",
            "title": "Заголовок(en)",
            "subtype": "Подкатегория недвижимости"
        }


class SearchConfigForm(forms.Form):
    email = forms.BooleanField(label='Отображать email', required=False)
    phone = forms.BooleanField(label='Отображать телефон', required=False)

    search_form = forms.BooleanField(label='Отображать форму', required=False)

    owner = forms.BooleanField(label='Отображать владельца', required=False)

    def __init__(self, *args, **kwargs):
        super(SearchConfigForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2 pt-3'
        self.helper.field_class = 'col-sm-10 pt-3'

        search_config = SearchConfig.objects.all().first()
        self.fields['email'].initial = search_config.show_email_field
        self.fields['phone'].initial = search_config.show_phone_field
        self.fields[
            'search_form'].initial = search_config.show_search_form_field
        self.fields['owner'].initial = search_config.show_owner_field


class SubsubsubtypeOfRealEstateForm(forms.ModelForm):
    subsubtype = SubsubtypeModelChoiceField(
        queryset=SubsubtypeOfRealEstate.objects.all(), label="Тип недвижиости")

    class Meta:
        model = SubsubsubtypeOfRealEstate
        fields = ('name', 'title_rus', 'title', 'subsubtype')
        labels = {
            "name": "Название(en)",
            "title_rus": "Заголовок(ру)",
            "title": "Заголовок(en)",
            "subsubtype": "Тип недвижиости"
        }


class CategoryForm(forms.ModelForm):
    parent_categories = CategoryModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('point'),
        label="Предок",
        required=False,
        widget=Select2MultipleWidget)

    def __init__(self, *args, **kwargs):
        query_parent_categories = kwargs.pop('parent_categories', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        try:
            if query_parent_categories:
                self.fields['parent_categories'].queryset = query_parent_categories
        except:
            pass

        self.fields['name'].widget.attrs.update(
            {'class': 'textinput textInput form-control'})
        self.fields['name_ru'].widget.attrs.update(
            {'class': 'textinput textInput form-control'})
        self.fields['comment'].widget.attrs.update(
            {'class': 'textinput textInput form-control'})
        self.fields['point'].widget.attrs.update(
            {'class': 'textinput textInput form-control'})

    class Meta:
        model = Category
        fields = ('name', 'name_ru', 'comment', 'point', 'parent_categories')
        labels = {
            "name": "Название(en)",
            "name_ru": "Название(ру)",
            "comment": "Описание",
            "point": "Пункт",
            "parent_categories": "Вышестоящий элемент"
        }

    def clean_name(self):
        print("ccall clean_name !!!")
        return clean_unique(self, 'name')


class ParameterForm(forms.ModelForm):
    parser_parameters = ParserParameterMultipleModelChoiceField(
        queryset=ParserParameter.objects.all().order_by('name_ru'),
        label="Параметры, собираемые парсерами",
        required=False)

    parser_parameters.widget.attrs.update({
        'class': 'parser-parameters-select'
    })

    unit = UnitModelChoiceField(queryset=Unit.objects.all(),
                                label="единица",
                                required=False)

    class Meta:
        model = Parameter
        fields = ('name', 'name_ru', 'is_load_file', 'is_comment', 'unit',
                  'parser_parameters')
        labels = {
            "name": "Название(en)",
            "name_ru": "Название(ру)",
            "is_load_file": "Добавлять файл",
            "is_comment": "Добавлять описание",
            "unit": "единица",
            "parser_parameters": "Параметры, собираемые парсерами"
        }


class ParametersForm(forms.Form):
    parameters_data = ParameterMultipleModelChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Parameter.objects.all(),
        label="Параметры")

    def __init__(self, *args, **kwargs):
        exist_parameters_query = kwargs.pop('exist_parameters', None)
        super(ParametersForm, self).__init__(*args, **kwargs)
        try:
            if exist_parameters_query:
                self.fields['parameters_data'].queryset = exist_parameters_query
        except:
            pass


class CategoriesForm(forms.Form):
    categories_data = CategoryModelMultipleChoiceField(
        widget=Select2MultipleWidget,
        queryset=Category.objects.all().order_by('point'),
        label="Категории")

    def __init__(self, *args, **kwargs):
        categories_data_query = kwargs.pop('exist_categories', None)
        super(CategoriesForm, self).__init__(*args, **kwargs)
        try:
            if categories_data_query:
                self.fields['categories_data'].queryset = categories_data_query
        except:
            pass


class UnitForm(forms.ModelForm):
    value_type = TypeOfValueModelChoiceField(
        queryset=TypeOfValue.objects.all(), label="Тип значения")

    class Meta:
        model = Unit
        fields = (
            'name',
            'name_ru',
            'value_type',
        )
        labels = {
            "name": "Название(en)",
            "name_ru": "Название(ру)",
            "value_type": "Тип значения",
        }


class TypeOfValueForm(forms.ModelForm):
    class Meta:
        model = TypeOfValue
        fields = ('name', 'name_ru')
        labels = {"name": "Название(en)", "name_ru": "Название(ру)"}


class ParserParameterForm(forms.ModelForm):
    parser_type = ParserParameterMultipleModelChoiceField(
        queryset=ParserType.objects.all(), label="Тип парсера", required=False)

    class Meta:
        model = ParserParameter
        fields = ('name', 'name_ru', 'parser_type')
        labels = {
            "name": "Название(en)",
            "name_ru": "Название(ру)",
            "parser_type": "Тип парсера"
        }


class ParserTypeForm(forms.ModelForm):
    class Meta:
        model = ParserType
        fields = ('name', 'name_ru', 'url', 'login', 'password', 'authkey')
        labels = {
            "name": "Название(en)",
            "name_ru": "Название(ру)",
            "url": "url",
            "login": "Логин",
            "password": "Пароль",
            "authkey": "Ключ"
        }


class ParserParametersListForm(forms.Form):
    parameters_data = ParserParameterMultipleModelChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=ParserParameter.objects.all(),
        label="Параметры парсера")

    def __init__(self, *args, **kwargs):
        parameters_data_query = kwargs.pop('exist_parameters', None)
        super(ParserParametersListForm, self).__init__(*args, **kwargs)
        try:
            if parameters_data_query:
                self.fields['parameters_data'].queryset = parameters_data_query
        except:
            pass


class FormSearchForm(forms.ModelForm):

    # categories = CategoryModelMultipleChoiceField(queryset = Category.objects.all(), widget = forms.CheckboxSelectMultiple,
    #                                                     label = "Категории")

    class Meta:
        model = SearchForm
        fields = ('name', 'name_ru', 'categories', 'user')
        labels = {
            "name": "Название(en)",
            "name_ru": "Название(ру)",
            "categories": "Категории",
            "user": "Пользователь"
        }

        widgets = {
            'user': forms.HiddenInput(),
            # 'categories': TreeWidget(),
        }

    def __init__(self, *args, **kwargs):
        user_query = kwargs.pop('user', None)
        super(FormSearchForm, self).__init__(*args, **kwargs)
        try:
            if user_query:
                self.fields['user'].initial = user_query
        except:
            pass
        self.fields['name'].widget.attrs.update(
            {'class': 'textinput textInput form-control'})
        self.fields['name_ru'].widget.attrs.update(
            {'class': 'textinput textInput form-control'})


class ViewSearchForm(forms.ModelForm):
    def add_category_value_field(self, formula_category, indx):
        field_name = 'category_value_%s' % (indx, )
        self.fields[field_name] = forms.CharField(required=False)
        try:
            self.initial[field_name] = formula_category.value
        except IndexError:
            self.initial[field_name] = ""

    def __init__(self, *args, **kwargs):

        exist_search_form = kwargs.pop('exist_search_form', None)

        super().__init__(*args, **kwargs)
        categories = []

        try:
            if exist_search_form:
                categories = exist_search_form.categories
                for i in range(len(categories) + 1):
                    temp_category = categories[i]
                    formula_category_list = FormulaCategory.objects.filter(
                        category=temp_category)
                    for formula_cat in formula_category_list:
                        add_category_value_field(self, formula_cat, i)
                        add_category_rate_field(self, formula_cat, i)
                        add_category_field(self, formula_cat, i)
        except:
            pass

    def add_category_rate_field(self, formula_category, indx):
        field_name = 'category_rate_%s' % (indx, )
        self.fields[field_name] = forms.CharField(required=False)
        try:
            self.initial[field_name] = formula_category.rate
        except IndexError:
            self.initial[field_name] = ""

    def add_category_field(self, formula_category, indx):
        field_name = 'category_formula_%s' % (indx, )
        self.fields[field_name] = forms.CharField(required=False)
        try:
            self.initial[field_name] = formula_category.formula
        except IndexError:
            self.initial[field_name] = ""


class ParameterDataForm(forms.ModelForm):
    class Meta:
        model = ParameterData
        fields = ('value', 'rate')
        labels = {
            "value": "Значение",
            "rate": "Вес",
        }


class TestForm(forms.Form):
    things = forms.CharField(widget=NodeInputWidget)
