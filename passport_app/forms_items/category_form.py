from django import forms
from passport_app.models import Category
from forms_fields.category_model_choice_field import CategoryModelChoiceField

class CategoryForm(forms.ModelForm):
    parent_category = CategoryModelChoiceField(queryset = SubsubtypeOfRealEstate.objects.all(),
                                            label="Родительская категория")

    class Meta:
        model = Category
        fields = ('name', 'name_ru', 'comment', 'categories', 'parameters')