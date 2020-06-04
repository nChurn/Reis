from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from passport_app.models import Category
from django.http import HttpResponse
from django.views import View
from django.template.loader import render_to_string
from passport_app.forms import CategoryForm, CategoriesForm, TestForm
from passport_app.models import FormulaCategory
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
            if len(parents_ids) > 0:     
                for parent_id in parents_ids:
                    parent = Category.objects.get(id = parent_id)
                    if parent:
                        category.save()                        
                        parent.categories.add(category)
                        if category.point is None:
                            if parent.categories.count() > 1:
                                children = parent.categories.extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                                    order_by('int_point').all()
                                arr = [x for x in children if x.id != category.id][-1].point.split('.')
                                arr[-1] = str(int(arr[-1]) + 1)
                                category.point = ".".join(arr)
                            else:
                                category.point = parent.point + '.1'
                        parent.save()
                        category.parent_categories.add(parent)   

                        f = FormulaCategory()                     
                        f.category = category
                        f.rate = 5
                        f.amount = parent.categories.count()
                        f.formula = 'x/y'
                        f.save()
            else:
                children = Category.objects.filter(parent_categories = None).extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                                    order_by('int_point').all()
                if children:
                    p = [x for x in children if x.id != category.id][-1].point
                    category.point = int(p) + 1

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
            categories = Category.objects.filter(name = category_name). \
                extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                order_by('int_point')           
        except:
            categories = Category.objects.filter(parent_categories = None). \
                extra(select={'myinteger': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                order_by('myinteger')

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
                    new_category = Category()
                    new_category.name = child_category.name
                    new_category.name_ru = child_category.name_ru
                    new_category.comment = child_category.comment
                    new_category.point = child_category.point
                    new_category.save()

                    category.categories.add(new_category)
                    new_category.parent_categories.add(category)
                    new_category.save()
        else:
            child_category_id = categories_data
            child_category = Category.objects.get(id=child_category_id)
            if child_category:
                new_category = Category()
                new_category.name = child_category.name
                new_category.name_ru = child_category.name_ru
                new_category.comment = child_category.comment
                new_category.point = child_category.point
                new_category.save()

                category.categories.add(new_category)
                new_category.parent_categories.add(category)
                new_category.save()

        category.save()
        for c in category.categories. \
                extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                order_by('int_point').all():
            self.recalc_points(c, category)
        return redirect('/constructor/#v-pills-category')

    def recalc_points(self, category, parent_category):
        i = 1
        category.point = parent_category.point + '.' + str(i)
        category.save()

        for child in category.categories. \
                extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                order_by('int_point').all():
            child.point = category.point + '.' + str(i)
            i = i + 1
            child.save()

            for c in child.categories. \
                    extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                    order_by('int_point').all():
                self.recalc_points(c, child)
                c.save()

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
            categories = category.categories. \
                extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                order_by('int_point').all()           
        except:      
            pass

        form = CategoryForm()
        html = render_to_string('category/category_child_nodes.html', {'categories_form': form, 'child_categories': categories, 'parent_category': category}, request=request)
        return HttpResponse(html)
        

class CategoryPaste(View):
    def post(self, request, *args, **kwargs):        
        target_category = Category.objects.get(id = request.POST.get('category_id_paste_in', None))
        copy_category = Category.objects.get(id = request.POST.get('category_copy_id', None))

        self.copy_categories(copy_category, target_category)
        return redirect('/constructor/#v-pills-category')

    def copy_categories(self, category, parent_category):
        new_category = self.create_copy_category(category, parent_category)
        if category.categories is not None:
            for child in category.categories. \
                    extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                    order_by('int_point').all():
                self.copy_categories(child, new_category)

    def create_copy_category(self, category, parent_category):
        new_category = Category()
        new_category.name = category.name
        new_category.name_ru = category.name_ru
        new_category.comment = category.comment

        last_children = parent_category.categories. \
                extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
                order_by('int_point').last()
        if last_children is not None:
            arr = last_children.point.split('.')
            arr[-1] = str(int(arr[-1]) + 1)
            new_category.point = ".".join(arr)
        else:
            new_category.point = parent_category.point + '.1'

        new_category.save()
        new_category.parent_categories.add(parent_category)
        new_category.save()
        parent_category.categories.add(new_category)
        parent_category.save()

        return new_category

class TemplateFormView(FormView):
    template_name = 'category/test_form.html'
    form_class = TestForm
    success_url = '/'