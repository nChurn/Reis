from django.views.generic import *
from passport_app.models import *
from passport_app.forms_items.rate_classifier_form import *

class RateClassifierListView(ListView):
    template_name = 'rate_classifier/classifier_container.html'
    model = RateClassifier

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = RateClassifierForm()
        return context

class RateClassifierCreateView(CreateView):
    model = RateClassifier
    fields = ['min_rate', 'max_rate', 'label', 'category']

    success_url = '/constructor/#v-pills-rate-classifier'

class RateClassifierUpdateView(UpdateView):
    model = RateClassifier
    fields = ['min_rate', 'max_rate', 'label', 'category']

    success_url = '/constructor/#v-pills-rate-classifier'
    template_name = 'rate_classifier/update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = RateClassifier.objects.get(pk=self.kwargs['pk'])
        context['form'] = RateClassifierForm(instance=obj)
        context['pk'] = self.kwargs['pk']
        return context

class RateClassifierDeleteView(DeleteView):
    model = RateClassifier
    template_name = 'rate_classifier/confirm_delete.html'
    success_url = '/constructor/#v-pills-rate-classifier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['obj'] = RateClassifier.objects.get(pk=self.kwargs['pk'])     
        context['pk'] = self.kwargs['pk']
        return context
