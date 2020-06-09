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
        categories = Category.objects.filter(parent_categories = None). \
            extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
            order_by('int_point')
        form_categories = search_form.categories.\
            extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
            order_by('int_point')

        html = render_to_string('search_form/partial_modal_edit.html', {
                'form': form,
                'id':search_form.id, 
                'categories':categories,
                'form_categories':form_categories
            }, request=request)
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
        categories = Category.objects.filter(parent_categories = None). \
            extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
            order_by('int_point')
        html = render_to_string('search_form/form_container.html', {'search_forms': searchforms, 'form': form, 'categories':categories, 'form_categories':[]}, request=request)
        return HttpResponse(html)

class ViewFormSearch(LoginRequiredMixin, View):
    def get_category_view_data(self, search_form, categories):
        view_data = {}
        view_data['categories'] = []
        
        if categories.exists():
            for form_cat_item in categories.all():
                if form_cat_item not in search_form.categories.all():
                    continue

                formula_list = FormulaCategory.objects.filter(category = form_cat_item, search_form = search_form)
                formula_parametrs = FormulaParameterCategory.objects.filter(category = form_cat_item)
                child_categories =  self.get_category_view_data(search_form, form_cat_item.categories. \
                    extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                    order_by('int_point'))
                category_data = { 
                    'formula': formula_list, 
                    'formula_parameters': formula_parametrs, 
                    'category': form_cat_item, 
                    'categories': child_categories
                }
                view_data['categories'].append(category_data)

        return view_data            

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        search_form = get_object_or_404(SearchForm, id=pk)
        form = FormSearchForm(instance=search_form) 
        # categories = Category.objects.filter(parent_categories = None). \
        #     extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
        #     order_by('int_point') 
        # form_categories = search_form.categories. \
        #     extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
        #     order_by('int_point') 
        view_category = search_form.categories.filter(parent_categories = None). \
            extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
            order_by('int_point')     
        view_data = self.get_category_view_data(search_form, view_category)
        
        html = render_to_string('search_form/view_form_content.html', {
            'form': form, 
            'id':search_form.id, 
            'search_form': search_form,
            #'categories':categories, 
            # 'form_categories': form_categories, 
            'view_data': view_data
        }, request=request)
        return HttpResponse(html)

    def set_category_view_data(self, search_form, params, categories):        
        if categories.exists():
            for form_cat_item in categories.all():
                #create data
                new_formula = FormulaCategory()
                new_formula.search_form = search_form
                new_formula.category = form_cat_item
                val_name = "formula_rate_create_%i" % (form_cat_item.id)
                rate = params.get(val_name, None)
                if rate:
                    new_formula.rate = rate

                rate_name = "formula_amount_create_%i" % (form_cat_item.id)
                amount = params.get(rate_name, None)
                if rate:
                    new_formula.amount = amount

                formula_name = "formula_create_%i" % (form_cat_item.id)
                formula = params.get(formula_name, None)

                if formula:
                    new_formula.formula = formula                        
                if amount or rate or formula:
                    new_formula.save()
                    continue

                #update data
                formula_list = FormulaCategory.objects.filter(category = form_cat_item)
                if formula_list.exists():
                    for formula_cat in formula_list:
                        val_name = "formula_rate_%i" % (formula_cat.id)
                        val = params.get(val_name, None)
                        if val:
                            formula_cat.rate = val

                        rate_name = "formula_amount_%i" % (formula_cat.id)
                        rate = params.get(rate_name, None)
                        if rate:
                            formula_cat.amount = rate

                        formula_name = "formula_%i" % (formula_cat.id)
                        formula = params.get(formula_name, None)

                        if formula:
                            formula_cat.formula = formula                        
                        formula_cat.save()


                #update parameter formulas
                #пока не работает
                params_list = FormulaParameterCategory.objects.filter(category = form_cat_item)
                if params_list.exists():
                    for formula_param in params_list:
                        formula_name = "parameter_formula_%i" % (formula_param.id)
                        parameter_formula = params.get(formula_name, None)
                        if parameter_formula:
                            formula_param.formula = parameter_formula
                            formula_param.save()

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        search_form = get_object_or_404(SearchForm, id=pk)
        view_category = search_form.categories

        search_form.formula_rate = request.POST.get('general_rate')
        search_form.formula_amount = request.POST.get('general_amount')
        search_form.formula = request.POST.get('general_formula')
        search_form.save()
        
        self.set_category_view_data(search_form, request.POST, view_category)

        return redirect("/constructor")

