from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

# Create your models here.
#=====================================================
class Country(models.Model):
    name = models.CharField(max_length=255, default='')

class Region(models.Model):
    name = models.CharField(max_length=255, default='')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

class District(models.Model):
    name = models.CharField(max_length=255, default='')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)

class TypeOfLocality(models.Model):
    name = models.CharField(max_length=255, default='')

class Locality(models.Model):
    name = models.CharField(max_length=255, default='')
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    type_of_locality = models.ForeignKey(TypeOfLocality, on_delete=models.CASCADE)

class TypeOfStreet(models.Model):
    name = models.CharField(max_length=255, default='')

class Street(models.Model):
    name = models.CharField(max_length=255, default='')
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, blank=True, null=True)
    type_of_street = models.ForeignKey(TypeOfLocality, on_delete=models.CASCADE)

##===============================================
class Classifier(models.Model):
    name = models.CharField(max_length=255, default='')
    point = models.CharField(max_length=10, default='')
    descr = models.CharField(max_length=255, default='')
    name_ru = models.CharField(max_length=255, default='')

class TypeOfValue(models.Model):
    name = models.CharField(max_length=255, unique = True, default='')
    name_ru = models.CharField(max_length=255, unique = True, default='')
    def get_absolute_url(self):
        return "/constructor" #reverse('constructor', kwargs={'pk': self.pk})

class Unit(models.Model):
    name = models.CharField(max_length=255, unique = True, default='')
    name_ru = models.CharField(max_length=255, unique = True, default='')
    value_type = models.ForeignKey(TypeOfValue, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return "/constructor" #reverse('constructor', kwargs={'pk': self.pk})



#================================================

class Owner(models.Model):
    name = models.CharField(max_length=255)
    inn = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

class TypeOfRealEstate(models.Model):
    name = models.CharField(max_length=255, default = '')
    title_rus = models.CharField(max_length=255, default = '')
    title = models.CharField(max_length=255, default = '')

class SubtypeOfRealEstate(models.Model):
    name = models.CharField(max_length=255, default = '')
    title_rus = models.CharField(max_length=255, default = '')
    title = models.CharField(max_length=255, default = '')
    type = models.ForeignKey(TypeOfRealEstate, related_name='type', on_delete=models.CASCADE)

class SubsubtypeOfRealEstate(models.Model):
    name = models.CharField(max_length=255, default = '')
    title_rus = models.CharField(max_length=255, default = '')
    title = models.CharField(max_length=255, default = '')
    subtype = models.ForeignKey(SubtypeOfRealEstate, related_name='subtype', on_delete=models.CASCADE)

class SubsubsubtypeOfRealEstate(models.Model):
    name = models.CharField(max_length=255, default = '')
    title_rus = models.CharField(max_length=255, default = '')
    title = models.CharField(max_length=255, default = '')
    subsubtype = models.ForeignKey(SubsubtypeOfRealEstate, related_name='subsubtype', on_delete=models.CASCADE)


class GroupVisit(models.Model):
    request_count = models.IntegerField(default=0)
    day_period = models.IntegerField(default=1)
    group = models.ForeignKey(Group, related_name='group', on_delete=models.CASCADE)

class UserVisit(models.Model):
    request_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='user_visit', on_delete=models.CASCADE)   


class Field(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    title_rus = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=True, null=True)
    classifier = models.ForeignKey(Classifier, related_name='classifier', on_delete=models.CASCADE)
    type_of_value = models.ForeignKey(TypeOfValue, on_delete=models.CASCADE, blank=True, null=True)
    point = models.CharField(max_length=20, default='')
    parser_type = models.IntegerField(default=0)

class UserUser(models.Model):
    creator_user = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='created_user', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

class NotLoginUserVisit(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=20, default='')

class SearchConfig(models.Model):
    show_phone_field = models.BooleanField(default=False)
    show_email_field = models.BooleanField(default=False)
    show_search_form_field = models.BooleanField(default=False)
    show_owner_field = models.BooleanField(default=False)

class Priority(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)
    name_ru = models.CharField(max_length=255, default='', unique=True)
    value = models.IntegerField(default=0)

class ParserType(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)
    name_ru = models.CharField(max_length=255, default='', unique=True)
    # parser_parameters = models.ManyToManyField(ParserParameter, blank=True, null=True)
    url = models.CharField(max_length=255, default='', blank=True, null=True)
    login = models.CharField(max_length=255, default='', blank=True, null=True)
    password = models.CharField(max_length=255, default='', blank=True, null=True)
    authkey = models.CharField(max_length=255, default='', blank=True, null=True)
    priority = models.ForeignKey(Priority, on_delete = models.SET_NULL, blank=True, null=True)
    def get_absolute_url(self):
        return "/constructor" #reverse('constructor', kwargs={'pk': self.pk})
    
class ParserParameter(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)
    name_ru = models.CharField(max_length=255, default='')
    parser_type = models.ForeignKey(ParserType, on_delete = models.CASCADE, blank=True, null=True)
    parser_parameter_type = models.CharField(max_length=255, default='')
    def get_absolute_url(self):
        return "/constructor" #reverse('constructor', kwargs={'pk': self.pk})

class Parameter(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)    
    name_ru = models.CharField(max_length=255, default='', unique=True)    
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=True, null=True)    
    parser_parameters = models.ManyToManyField(ParserParameter, blank=True)    
    is_load_file = models.BooleanField(default=False, blank=True)
    is_comment = models.BooleanField(default=False, blank=True)
    def get_absolute_url(self):
        return "/constructor" #reverse('constructor', kwargs={'pk': self.pk})

class Category(models.Model):
    name = models.CharField(max_length=255, default='')#, unique=True)
    name_ru = models.CharField(max_length=255, default='')    
    comment = models.CharField(max_length=255, default='', blank=True)
    point = models.CharField(max_length=20, default='')
    categories = models.ManyToManyField("self", related_name='childs', symmetrical=False, blank=True, null=True)
    parameters = models.ManyToManyField(Parameter, blank=True, null=True)
    parent_categories = models.ManyToManyField("self", related_name='parent', symmetrical=False, blank=True, null=True)
    # parent_category = models.ForeignKey("passport_app.Category", on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    def get_absolute_url(self):
        return "/constructor" #reverse('category-detail', kwargs={'pk': self.id})

class SearchForm(models.Model):
    config = models.TextField(default="")
    name = models.CharField(max_length=255, default = "", unique = True)
    name_ru = models.CharField(max_length=255, default = "")
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True, null=True)
    
    def get_absolute_url(self):
        return "/constructor"

class RealEstate(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    owner = models.ForeignKey(Owner, on_delete = models.CASCADE)
    #address
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True) # todo temporary
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, blank=True, null=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house_number = models.CharField(max_length=5, default='')
    korpus_number = models.CharField(max_length=5, default='')
    building_number = models.CharField(max_length=5, default='')
    flat_number = models.IntegerField(default=0)
    kadastr_number = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=255, default='')
    create_date = models.DateTimeField(auto_now=True, blank=True)
    subtype = models.ForeignKey(SubtypeOfRealEstate, on_delete=models.CASCADE, blank=True, null=True)
    subsubtype = models.ForeignKey(SubsubtypeOfRealEstate, on_delete=models.CASCADE, blank=True, null=True)
    search_form =  models.ForeignKey(SearchForm, on_delete=models.CASCADE, blank=True, null=True)
    country_name = models.CharField(max_length=255, default='')
    region_name = models.CharField(max_length=255, default='')
    district_name = models.CharField(max_length=255, default='') #область
    locality_name = models.CharField(max_length=255, default='') # населенный пункт
    street_name = models.CharField(max_length=255, default='') # населенный пункт
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    categories = models.ManyToManyField(Category) 
    report_number = models.IntegerField(default=0)

    
class DataField(models.Model):
    value = models.TextField(default="")
    rate = models.FloatField(default=0.0)
    validity = models.BooleanField(default=True)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, related_name='field', on_delete=models.CASCADE)


class ParameterData(models.Model):    
    value = models.TextField(default="")
    rate = models.FloatField(default=0.0)
    comment = models.CharField(max_length=255, default='')
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)

class ParserParameterData(models.Model):    
    value = models.TextField(default="")
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    parser_parameter = models.ForeignKey(ParserParameter, on_delete=models.CASCADE)

class FormulaCategory(models.Model):
    rate = models.CharField(max_length=255, default='')
    amount = models.CharField(max_length=255, default='')
    formula = models.CharField(max_length=255, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
class FormulaParameterCategory(models.Model):
    value_label = models.CharField(max_length=15, default='', unique=True)
    value = models.CharField(max_length=255, default='')
    rate_label = models.CharField(max_length=15, default='', unique=True)
    rate = models.CharField(max_length=255, default='')
    formula_label = models.CharField(max_length=15, default='', unique=True)
    formula = models.CharField(max_length=255, default='')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
