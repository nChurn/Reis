from django.forms import ModelChoiceField

class SearchFormModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name_ru