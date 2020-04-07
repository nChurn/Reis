from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from passport_app.models import TypeOfValue
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from passport_app.forms import TypeOfValueForm
from django.http import HttpResponseRedirect

class TypeOfValueCreate(CreateView):
    model = TypeOfValue
    fields = ['name', 'name_ru']

class TypeOfValueUpdate(UpdateView):
    model = TypeOfValue
    fields = ['name','name_ru']

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        type_of_value = get_object_or_404(TypeOfValue, id=pk)
        form = TypeOfValueForm(instance=type_of_value)
        html = render_to_string('type_of_value/partial_modal_edit.html', {'type_of_value_form': form, 'id':type_of_value.id}, request=request)
        return HttpResponse(html)

class TypeOfValueDelete(DeleteView):
    model = TypeOfValue
    success_url =  '/constructor/#v-pills-typeofvalue'
    success_message = "%(name)s was deleted successfully"
    
    def get(self, request, *args, **kwargs):
        type_of_value_id = None
        type_of_value = None

        try:
            type_of_value_id = self.kwargs['pk']
            type_of_value = get_object_or_404(TypeOfValue, id = type_of_value_id)      
        except:                 
            pass

        html = render_to_string('type_of_value/confirm_delete.html', {'object': type_of_value}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        type_of_value_id = None
        type_of_value = None

        type_of_value_id = self.kwargs['pk']
        type_of_value = get_object_or_404(TypeOfValue, id = type_of_value_id)      
        type_of_value.delete()
        return redirect('/constructor/#v-pills-typeofvalue')

class TypeOfValueSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        typeofvalue_name = None
        type_of_values = []

        try:
            unit_name = self.kwargs['name']
            type_of_values = TypeOfValue.objects.filter(name = typeofvalue_name, name_ru = typeofvalue_name)
        except:
            type_of_values = TypeOfValue.objects.all()  
            pass
        form = TypeOfValueForm()
        html = render_to_string('type_of_value/typeofvalue_container.html', {'type_of_values': type_of_values, 'type_of_value_form': form}, request=request)
        return HttpResponse(html)
