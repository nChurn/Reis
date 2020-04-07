from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from passport_app.models import SearchForm, Category, FormulaCategory, FormulaParameterCategory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from passport_app.forms import FormSearchForm
from django.http import HttpResponseRedirect

class SearchFormCreate(CreateView):
    model = SearchForm
    fields = ['name', 'name_ru', 'user', 'categories']
    

class SearchFormUpdate(UpdateView):
    model = SearchForm
    fields = ['name','name_ru', 'user', 'categories']

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        search_form = get_object_or_404(SearchForm, id=pk)
        form = FormSearchForm(instance=search_form)
        categories = Category.objects.filter(parent_categories = None)
        form_categories = search_form.categories
        html = render_to_string('search_form/partial_modal_edit.html', {'form': form, 'id':search_form.id, 'categories':categories, 'form_categories':form_categories}, request=request)
        return HttpResponse(html)

class SearchFormDelete(DeleteView):
    model = SearchForm
    success_url = "/constructor/"

class SearchFormSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form_name = None
        searchforms = []

        try:
            form_name = self.kwargs['name']
            searchforms = SearchForm.objects.filter(name = unit_name, name_ru = unit_name)
        except:
            searchforms = SearchForm.objects.all()  
            pass
        form = FormSearchForm(user=request.user)
        categories = Category.objects.filter(parent_categories = None)
        html = render_to_string('search_form/form_container.html', {'search_forms': searchforms, 'form': form, 'categories':categories, 'form_categories':[]}, request=request)
        return HttpResponse(html)

class ViewFormSearch(LoginRequiredMixin, View):

    def get_category_view_data(self, categories):
        view_data = {}
        view_data['categories'] = []
        
        if categories.exists():
            for form_cat_item in categories.all():
                formula_list = FormulaCategory.objects.filter(category = form_cat_item)
                formula_parametrs = FormulaParameterCategory.objects.filter(category = form_cat_item)
                child_categories =  self.get_category_view_data(form_cat_item.categories)
                category_data = { 'formula': formula_list, 'formula_parameters': formula_parametrs, 'category': form_cat_item, 'categories': child_categories}
                view_data['categories'].append(category_data)

        return view_data

    def set_category_view_data(self, params, categories):
        print(params)
        if categories.exists():
            for form_cat_item in categories.all():

                formula_list = FormulaCategory.objects.filter(category = form_cat_item)
                if formula_list.exists() :
                    for formula_cat in formula_list:
                        val_name = "category_value_%i" % (formula_cat.id)
                        val = params.get(val_name, None)
                        print(val_name)
                        print(val)
                        if val:
                            formula_cat.value = val

                        rate_name = "category_rate_%i" % (formula_cat.id)
                        rate = params.get(rate_name, None)
                        print(rate_name)
                        print(rate)
                        if rate:
                            formula_cat.rate = rate

                        formula_name = "category_formula_%i" % (formula_cat.id)
                        formula = params.get(formula_name, None)
                        print(formula_name)
                        print(formula)

                        if formula:
                            formula_cat.formula = formula                        
                        formula_cat.save()

                params_list = FormulaParameterCategory.objects.filter(category = form_cat_item)
                if params_list.exists():
                    for formula_param in params_list:

                        formula_name = "parameter_formula_%i" % (formula_param.id)
                        parameter_formula = params.get(formula_name, None)
                        if parameter_formula:
                            formula_param.formula = parameter_formula
                            formula_param.save()
        

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        search_form = get_object_or_404(SearchForm, id=pk)
        form = FormSearchForm(instance=search_form) 
        categories = Category.objects.filter(parent_categories = None)
        form_categories = search_form.categories
        view_category = search_form.categories.filter(parent_categories = None)
        view_data = self.get_category_view_data(view_category)
        
        # html = render_to_string('search_form/form_container.html', { 'search_forms': searchforms, 'form': form, 'categories':categories, 'form_categories':form_categories, 
        # 'view_form_categories':view_data}, request=request)
        # return HttpResponse(html)

        html = render_to_string('search_form/view_form_content.html', {'form': form, 
        'id':search_form.id, 
        'categories':categories, 
        'form_categories':form_categories, 
        'view_data': view_data}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        search_form = get_object_or_404(SearchForm, id=pk)
        view_category = search_form.categories
        
        self.set_category_view_data(request.POST, view_category)

        return redirect("/constructor")

