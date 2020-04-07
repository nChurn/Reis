from django.forms import ModelChoiceField
from django.forms import ModelMultipleChoiceField

class CategoryModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name_ru

class CategoryModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return '%s %s' % (obj.point, obj.name_ru)

class ParameterModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name_ru

class ParameterMultipleModelChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name_ru

class ParameterMultipleModelChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name_ru

class ParserParameterMultipleModelChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name_ru

class UnitModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name_ru

class TypeOfValueModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name_ru