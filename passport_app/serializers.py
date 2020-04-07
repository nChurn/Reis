from django.contrib.auth.models import User, Group
from rest_framework import serializers
from passport_app.models import *

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name', 'id', )
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'id', 'first_name', 'last_name')
        read_only_fields = ['id']



class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ['name', 'patronymic', 'last_name']

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ['name']

class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ['name']

class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        fields = ['name']

class TypeOfLocalitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeOfLocality
        fields = ['name']

class LocalitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locality
        fields = ['name']

class TypeOfStreetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeOfStreet
        fields = ['name']

class StreetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Street
        fields = ['name']

class ClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classifier
        fields = ['name', 'point', 'descr', 'name_ru', 'id']
        read_only_fields = ['id']

class TypeOfValueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeOfValue
        fields = ['name']

class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ['name']

class FieldSerializer(serializers.ModelSerializer):
    # classifier = ClassifierSerializer(many=False, read_only=True)
    class Meta:
        model = Field
        fields = ['id', 'name', 'title', 'title_rus', 'point', 'classifier']
        read_only_fields = ['id']

class DataFieldSerializer(serializers.ModelSerializer):
    field = FieldSerializer(many=False, read_only=True)
    class Meta:
        model = DataField
        fields = ['validity', 'value', 'rate', 'field', 'id']
        read_only_fields = ['id']

class RealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstate
        fields = ['build_number', 'korpus_number', 'building_number', 'flat_number', 'create_date', 'id']
        read_only_fields = ['id']

class TypeOfRealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfRealEstate
        fields = ['id', 'name', 'title', 'title_rus']
        read_only_fields = ['id']


class SubtypeOfRealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtypeOfRealEstate
        fields = ['id', 'name', 'title', 'title_rus', 'type']
        read_only_fields = ['id']

class SubsubtypeOfRealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubsubtypeOfRealEstate
        fields = ['id', 'name', 'title', 'title_rus', 'subtype']
        read_only_fields = ['id']

class SubsubsubtypeOfRealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubsubsubtypeOfRealEstate
        fields = ['id', 'name', 'title', 'title_rus', 'subtype']
        read_only_fields = ['id']

class SearchFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchForm
        fields = ['id', 'name', 'name_ru', 'config', 'user', 'is_default']
        read_only_fields = ['id']


class GroupVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupVisit
        fields = ['id', 'request_count', 'day_period', 'group']
        read_only_fields = ['id']

class UserVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVisit
        fields = ['id', 'request_date', 'user_visit']
        read_only_fields = ['id']

class UserUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUser
        fields = ['id', 'create_date', 'creator', 'created_user']
        read_only_fields = ['id']


class NotLoginUserVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotLoginUserVisit
        fields = ['id', 'create_date', 'phone', 'email']
        read_only_fields = ['id']

