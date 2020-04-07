from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from passport_app.models import Parameter, Category, FormulaParameterCategory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from passport_app.forms import ParameterForm
from passport_app.forms import ParametersForm
from django.http import HttpResponseRedirect
from passport_app.print_exception import *

class ParameterCreate(CreateView):
    model = Parameter
    fields = ['name', 'name_ru', 'is_load_file', 'is_comment', 'unit', 'parser_parameters']

class ParameterUpdate(UpdateView):
    model = Parameter
    fields = ['name','name_ru', 'is_load_file', 'is_comment','unit', 'parser_parameters']

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        parameter = get_object_or_404(Parameter, id=pk)
        form = ParameterForm(instance=parameter)
        html = render_to_string('parameter/partial_modal_edit.html', {'parameter_form': form, 'id':parameter.id}, request=request)
        return HttpResponse(html)

class ParameterDelete(DeleteView):
    model = Parameter
    success_url = "/constructor/" #reverse_lazy('category-list')

class ParametersSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        parameter_name = None
        parameters = []

        try:
            parameter_name = self.kwargs['name']
            parameters = Parameter.objects.filter(name = parameter_name, name_ru = parameter_name)
        except:
            parameters = Parameter.objects.all()  
            pass
        form = ParameterForm()
        html = render_to_string('parameter/parameter_container.html', {'parameters': parameters, 'parameter_form': form}, request=request)
        return HttpResponse(html)

class ParametersAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):        
        parameters = Parameter.objects.all()
        cateory_id = int(self.kwargs['category_pk'])
        category = get_object_or_404(Category, id=cateory_id)
        if category.parameters:
            category_parametrs_ids = category.parameters.values('id')
            parameters = parameters.exclude(id__in=category_parametrs_ids)
        # form = ParametersForm()
        form = ParametersForm(exist_parameters = parameters.order_by('name_ru'))
        html = render_to_string('parameter/partial_modal_parameters_list.html', {'parameters_form': form, 'id':cateory_id}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        try:
            parameters = []
            cateory_id = self.kwargs['category_pk']
            category = get_object_or_404(Category, id=cateory_id)
            parameters_ids = request.POST.getlist('parameters_data')
            if isinstance(parameters_ids, list):
                for parameter_id in parameters_ids:
                    parameter = Parameter.objects.get(id=parameter_id)                
                    category.parameters.add(parameter)
                    parameter_formula = FormulaParameterCategory()
                    parameter_formula.category = category
                    parameter_formula.parameter = parameter
                    parameter_formula.value_label = "PV_%i_%i" % (parameter.id,category.id,)
                    parameter_formula.rate_label = "PR_%i_%i" % (parameter.id,category.id,)
                    parameter_formula.formula_label = "PF_%i_%i" % (parameter.id,category.id,)
                    parameter_formula.value = "PV_%i_%i" % (parameter.id,category.id,)
                    parameter_formula.rate = "PR_%i_%i" % (parameter.id,category.id,)
                    parameter_formula.save()
            else:
                parameter_id = parameters_ids
                parameter = Parameter.objects.get(id=parameter_id)
                category.parameters.add(parameter)
                parameter_formula = FormulaParameterCategory()
                # parameter_formula.value = "V_%i" % (parameter.id,)
                # parameter_formula.rate = "R_%i" % (parameter.id,)
                parameter_formula.category = category
                parameter_formula.parameter = parameter
                parameter_formula.value_label = "PV_%i_%i" % (parameter.id,category.id,)
                parameter_formula.rate_label = "PR_%i_%i" % (parameter.id,category.id,)
                parameter_formula.formula_label = "PF_%i_%i" % (parameter.id,category.id,)
                parameter_formula.value = "PV_%i_%i" % (parameter.id,category.id,)
                parameter_formula.rate = "PR_%i_%i" % (parameter.id,category.id,)
                parameter_formula.save()

            category.save()
        except Exception as e:
            PrintException()
            pass

        return redirect("/constructor/#v-pills-category")

class ParametersRemoveView(LoginRequiredMixin, View):

    def delete(self, request, *args, **kwargs):        
        cateory_id = self.kwargs['category_pk']
        parameter_id = self.kwargs['parameter_pk']
        category = get_object_or_404(Category, id=cateory_id)
        parameter = get_object_or_404(Parameter, id=parameter_id)
        category.parameters.remove(parameter)
        category.save()
        parameter_formula = FormulaParameterCategory.objects.filter(parameter = parameter, category = category)
        if parameter_formula.exists():
            for formula in parameter_formula:
                formula.delete()
        next_url = request.GET.get('constructor', '')
        return HttpResponseRedirect(next_url)

# class ParameterFind(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         parameter_id = int(request.GET.get('id'))
#         parameter = Parameter.objects.get(id = category_id)
#         parameters = parameter.categories
#         parameter_parameters = category.parameters

#         html = render_to_string('categories_list.html', {'categories': categories, 'category_parameters': category_parameters}, request=request)
#         return HttpResponse(html)
