from django import forms
from passport_app.models import *

from django.forms.widgets import Select

class RateClassifierForm(forms.ModelForm):
    category = forms.ChoiceField(choices=[(obj.id, obj.name_ru) for obj in Category.objects.all()],
        label="Для категории"
    )
    category.widget.attrs.update({'style': 'width:100%;max-width:90%;'})

    class Meta:
        model = RateClassifier
        fields = ['min_rate', 'max_rate', 'label']
        labels = {
            'min_rate': 'Минимальный рейтинг',
            'max_rate': 'Максимальный рейтинг',
            'label': 'Текст классификатора',
        }