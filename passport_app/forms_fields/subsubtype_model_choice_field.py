from django.forms import ModelChoiceField

class SubsubtypeModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title_rus
