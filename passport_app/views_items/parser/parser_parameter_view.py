from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from passport_app.models import ParserParameter, ParserType
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from passport_app.forms import ParserParameterForm, ParserParametersListForm
from django.http import HttpResponseRedirect

class ParserParameterCreate(CreateView):
    model = ParserParameter
    fields = ['name']

class ParserParameterUpdate(UpdateView):
    model = ParserParameter
    fields = ['name']

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        parameter = get_object_or_404(ParserParameter, id=pk)
        form = ParserParameterForm(instance=parameter)
        html = render_to_string('parser/partial_modal_edit.html', {'parser_type_form': form, 'id':parameter.id}, request=request)
        return HttpResponse(html)

class ParserParameterDelete(DeleteView):
    model = ParserParameter
    success_url = "/constructor/" #reverse_lazy('category-list')
    success_message = "%(name)s was deleted successfully"
    # success_url = reverse_lazy("passport_app:constructor")
    def get(self, request, *args, **kwargs):
        parserparameter_id = None
        parserparameter = None

        try:
            parserparameter_id = self.kwargs['pk']
            parserparameter = get_object_or_404(ParserParameter, id = parserparameter_id)      
        except:                 
            pass

        html = render_to_string('parser/confirm_delete.html', {'object': parserparameter}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        parserparameter_id = None
        parserparameter = None

        parserparameter_id = self.kwargs['pk']
        parserparameter = get_object_or_404(ParserParameter, id = parserparameter_id)      
        parserparameter.delete()
        return redirect('/constructor/#v-pills-category')

class ParserParametersSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        parser_parameter_name = None
        parameters = []

        try:
            parser_parameter_name = self.kwargs['name']
            parameters = Parameter.objects.filter(name = parameter_name)
        except:
            parameters = Parameter.objects.all()  
            pass
        form = ParserParameterForm()
        html = render_to_string('parser/parameter_container.html', {'parser_parameters': parameters, 'parser_type_form': form}, request=request)
        return HttpResponse(html)

class ParserParametersAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):        
        parser_parameters = []
        parser_parameter_ids = []
        parser_type_id = int(self.kwargs['parser_type_pk'])
        parser_type = get_object_or_404(ParserType, id=parser_type_id)
        parser_parameters = ParserParameter.objects.all()

        if parser_type and parser_type.parser_parameters:
            exist_parser_parameters_ids = parser_type.parser_parameters.values_list('id', flat=True)
            parser_parameters = parser_parameters.exclude(id__in=exist_parser_parameters_ids)       
        form = ParserParametersListForm(exist_parameters = parser_parameters)
        html = render_to_string('parser/partial_modal_parameters_list.html', {'parser_parameters_list_form': form, 'id':parser_type_id}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        parser_type_id = self.kwargs['parser_type_pk']        
        parser_type = get_object_or_404(ParserType, id=parser_type_id)       
        parameters_data = []
        try:
            form_value = request.POST.copy()       
            parameters_data = form_value.getlist('parameters_data')
        except Exception as e:
            print(str(e))

        if parameters_data:
            for parser_parameter_id in parameters_data:
                parser_parameter = ParserParameter.objects.get(id=parser_parameter_id)
                if parser_parameter:
                    parser_type.parser_parameters.add(parser_parameter)
                    parser_type.save()
                    
        parser_type.save()
        return redirect('/constructor/#v-pills-category')

class ParserParametersDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):        
        parser_type_id = self.kwargs['parser_type_pkparser_type_pk']
        parser_parameter_id = self.kwargs['parser_parameter_pk']        
        parser_type = get_object_or_404(ParserType, id=parser_type_id)
        parser_parameter = get_object_or_404(ParserParameter, id=parser_parameter_id)
        parser_type.parser_parameters.remove(parser_parameter)
        parser_type.save()       
        return redirect('/constructor/#v-pills-category')        
