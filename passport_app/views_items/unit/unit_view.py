from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from passport_app.models import Unit
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from passport_app.forms import UnitForm
from django.http import HttpResponseRedirect

class UnitCreate(CreateView):
    model = Unit
    fields = ['name', 'name_ru', 'value_type']

class UnitUpdate(UpdateView):
    model = Unit
    fields = ['name','name_ru', 'value_type']

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        unit = get_object_or_404(Unit, id=pk)
        form = UnitForm(instance=unit)
        html = render_to_string('unit/partial_modal_edit.html', {'unit_form': form, 'id':unit.id}, request=request)
        return HttpResponse(html)

class UnitDelete(DeleteView):
    model = Unit
    success_url =  '/constructor/#v-pills-unit'
    success_message = "%(name)s was deleted successfully"
    
    def get(self, request, *args, **kwargs):
        unit_id = None
        unit = None

        try:
            unit_id = self.kwargs['pk']
            unit = get_object_or_404(Unit, id = unit_id)      
        except:                 
            pass

        html = render_to_string('unit/confirm_delete.html', {'object': unit}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        unit_id = None
        unit = None

        unit_id = self.kwargs['pk']
        unit = get_object_or_404(Unit, id = unit_id)      
        unit.delete()
        return redirect('/constructor/#v-pills-unit')

class UnitSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        unit_name = None
        units = []

        try:
            unit_name = self.kwargs['name']
            units = Unit.objects.filter(name = unit_name, name_ru = unit_name)
        except:
            units = Unit.objects.all()  
            pass
        form = UnitForm()
        html = render_to_string('unit/unit_container.html', {'units': units, 'unit_form': form}, request=request)
        return HttpResponse(html)
