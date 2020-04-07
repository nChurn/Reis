from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from passport_app.models import ParserType, ParserParameter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from passport_app.forms import ParserTypeForm, ParserParameterForm
from django.http import HttpResponseRedirect

class ParserTypeCreate(CreateView):
    model = ParserType
    fields = ['name', 'name_ru', 'url', 'login', 'password', 'authkey']    

class ParserTypeUpdate(UpdateView):
    model = ParserType
    fields = ['name', 'name_ru', 'url', 'login', 'password', 'authkey']    

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        parser_type = get_object_or_404(ParserType, id=pk)
        form = ParserTypeForm(instance=parser_type)
        html = render_to_string('parser/partial_modal_edit.html', {'parser_type_form': form, 'id':parser_type.id}, request=request)
        return HttpResponse(html)

class ParserTypeDelete(DeleteView):
    model = ParserType
    success_url = "/constructor/"
    success_message = "%(name)s was deleted successfully"
    # success_url = reverse_lazy("passport_app:constructor")
    def get(self, request, *args, **kwargs):
        parsertype_id = None
        parsertype = None

        try:
            parsertype_id = self.kwargs['pk']
            parsertype = get_object_or_404(ParserType, id = parsertype_id)      
        except:                 
            pass

        html = render_to_string('parser/confirm_delete.html', {'object': parsertype}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        parsertype_id = None
        parsertype = None

        parsertype_id = self.kwargs['pk']
        parsertype = get_object_or_404(ParserType, id = parsertype_id)      
        parsertype.delete()
        return redirect('/constructor/#v-pills-category')


class ParserTypeSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        parser_type_name = None
        parser_types = []

        try:
            parser_type_name = self.kwargs['name']
            parser_types = ParserType.objects.filter(name = parser_type_name, name_ru = parser_type_name)
        except:
            parser_types = ParserType.objects.all()  
            pass
        form = ParserTypeForm()
        parser_parameter_form = ParserParameterForm()
        parser_parameters = ParserParameter.objects.all()
        html = render_to_string('parser/parser_container.html', {'parser_types': parser_types, 'parser_type_form': form, 'parser_parameter_form': parser_parameter_form, 'parser_parameters': parser_parameters}, request=request)
        return HttpResponse(html)
