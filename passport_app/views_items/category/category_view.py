from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from passport_app.models import Category
from django.http import HttpResponse
from django.views import View
from django.template.loader import render_to_string
from passport_app.forms import CategoryForm, CategoriesForm, TestForm
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import FormView


class CategoryDetails(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk'] #int(request.GET.get('pk')) #self.kwargs['pk']
        category = Category.objects.get(id = pk)        
        html = render_to_string('category/category_detail.html', {'category': category}, request=self.request)
        return HttpResponse(html)

class CategoryList(ListView):
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(parent_categories = None)

    def render_to_response(self, context):
        categories = Category.objects.filter(parent_categories = None)
        form = CategoryForm()
        html = render_to_string('category/category_list_view.html', {'categories': categories, 'form': form})
        return HttpResponse(html)

class CategoryCreate(CreateView):
    model = Category
    fields = ['name', 'name_ru', 'comment', 'point', 'parent_categories']
    def post(self, request):
        
        super(CategoryCreate, self).post(request)        
        form = CategoryForm(request.POST)        
        parents_ids = None
        try:
            form_value = request.POST.copy()       
            parents_ids = form_value.getlist('parent_categories')
        except Exception as e:
            print(str(e))

        try:
            category = Category.objects.get(name = request.POST['name'])
            if parents_ids:    
                if isinstance(parents_ids, list):     
                    for parent_id in parents_ids:
                        parent = Category.objects.get(id = parent_id)
                        if parent:
                            category.save()                        
                            parent.categories.add(category)
                            parent.save()
                            print(parent.categories)
                            category.parent_categories.add(parent)                        
                else:
                    parent = Category.objects.get(id = parents_ids)
                    if parent:
                        category.save()                        
                        parent.categories.add(category)
                        parent.save()
                        print(parent.categories)
                        category.parent_categories.add(parent)                        

            category.save()            
        except Exception as e:
            print(str(e))
            pass        
        return redirect('/constructor/#v-pills-category')

class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name', 'name_ru', 'comment', 'point', 'parent_categories']
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        category = get_object_or_404(Category, id=pk)
        form = CategoryForm(instance=category, parent_categories = Category.objects.all().exclude(id__in=[pk]))
        html = render_to_string('category/category_modal_edit.html', {'form': form, 'id':category.id}, request=request)
        return HttpResponse(html)

    def post(self, request, **kwargs):
        pk = self.kwargs['pk']
        category = Category.objects.get(id = pk)
        parents_ids = None
        try:
            form_value = request.POST.copy()       
            parents_ids = form_value.getlist('parent_categories')
        except Exception as e:
            print(str(e))

        if parents_ids:
            if category.parent_categories.all():
                parent_categories = category.parent_categories.all()
                print (parent_categories)
                for parent_category in parent_categories:
                    parent_category.categories.remove(category)
                    parent_category.save()
                    category.parent_categories.remove(parent_category)
                    category.save()

        super(CategoryUpdate, self).post(request, **kwargs)
        form = CategoryForm(request.POST)
        try:
            category = Category.objects.get(name = request.POST['name'])
            if parents_ids:                
                if isinstance(parents_ids, list):
                    for parent_id in parents_ids:
                        parent = Category.objects.get(id = parent_id)
                        if parent:
                            parent.categories.add(category)
                            parent.save()
                            category.parent_categories.add(parent)
                else:
                    parent = Category.objects.get(id = parents_ids)
                    if parent:
                        parent.categories.add(category)
                        parent.save()
                        category.parent_categories.add(parent)
                # if category.parent_categories:
                #     category.parent_category.categories.remove(category)                    
                parent = Category.objects.get(id = request.POST['parent_categories'])
                parent.categories.add(category)
                parent.save()
            category.save()            
        except Exception as e:
            print(str(e))
            pass
        return redirect('/constructor/#v-pills-category')


class CategoryDelete(DeleteView):
    model = Category
    success_url =  '/constructor/#v-pills-category'
    success_message = "%(name)s was deleted successfully"
    # success_url = reverse_lazy("passport_app:constructor")
    def get(self, request, *args, **kwargs):
        category_id = None
        category = None

        try:
            category_id = self.kwargs['pk']
            category = get_object_or_404(Category, id = category_id)      
        except:                 
            pass

        html = render_to_string('category/confirm_delete.html', {'object': category}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        category_id = None
        category = None

        category_id = self.kwargs['pk']
        category = get_object_or_404(Category, id = category_id)      
        category.delete()
        return redirect('/constructor/#v-pills-category')

class CategoriesSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category_name = None
        categories = []

        try:
            category_name = self.kwargs['name']
            categories = Category.objects.filter(name = category_name).order_by('id')           
        except:
            categories = Category.objects.filter(parent_categories = None).order_by('id')

        form = CategoryForm()
        html = render_to_string('category/category_container.html', {'categories': categories, 'form': form}, request=request)
        return HttpResponse(html)

class CategoryFind(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category_id = int(request.GET.get('id'))
        category = Category.objects.get(id = category_id)
        categories = category.categories
        category_parameters = category.parameters
        form = CategoryForm()
        html = render_to_string('categories_list.html', {'categories': categories, 'form': form}, request=request)
        return HttpResponse(html)

class CategoriesAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):        
        categories = []
        child_category_ids = []
        category_id = int(self.kwargs['category_pk'])
        category = get_object_or_404(Category, id=category_id)
        categories = Category.objects.all().exclude(id__in=[category.id])  

        if category and category.categories:
            child_category_ids = category.categories.values_list('id', flat=True)
            categories = categories.exclude(id__in=child_category_ids)       
        form = CategoriesForm(exist_categories = categories)
        html = render_to_string('category/partial_modal_parameters_list.html', {'categories_form': form, 'id':category_id}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        cateory_id = self.kwargs['category_pk']
        print(cateory_id)
        category = get_object_or_404(Category, id=cateory_id)
        categories_data = self.request.POST.get('categories_data')
        print(categories_data)
        if isinstance(categories_data, list):
            for child_category_id in categories_data:
                child_category = Category.objects.get(id=child_category_id)
                if child_category:
                    # if child_category.parent_categories:
                    #     child_category.parent_categories.categories.remove(child_category)
                    category.categories.add(child_category)
                    child_category.parent_categories.add(category)
                    child_category.save()
        else:
            child_category_id = categories_data
            child_category = Category.objects.get(id=child_category_id)
            if child_category:
                # if child_category.parent_categories:
                #         child_category.parent_categories.categories.remove(child_category)
                category.categories.add(child_category)
                child_category.parent_categories.add(category)
                child_category.save()

        category.save()
        return redirect('/constructor/#v-pills-category')

class CategoriesDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):        
        cateory_id = self.kwargs['category_pk']
        child_category_id = self.kwargs['child_category_pk']
        print(child_category_id)
        category = get_object_or_404(Category, id=cateory_id)
        child_category = get_object_or_404(Category, id=child_category_id)
        child_category.parent_categories.remove(category)
        child_category.save()
        category.categories.remove(child_category)
        category.save()
        next_url = request.GET.get('constructor', '')
        
        return redirect('/constructor/#v-pills-category')

class CategoriesParent(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category_id = None
        categories = []
        category = None
        try:
            category_id = self.kwargs['parent']
            category = Category.objects.get(id = category_id)
            categories = category.categories.all().order_by('point')           
        except:      
            pass

        form = CategoryForm()
        html = render_to_string('category/category_child_nodes.html', {'categories_form': form, 'child_categories': categories, 'parent_category': category}, request=request)
        return HttpResponse(html)
        

class TemplateFormView(FormView):
    template_name = 'category/test_form.html'
    form_class = TestForm
    success_url = '/'