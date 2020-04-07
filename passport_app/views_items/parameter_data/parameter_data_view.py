from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from passport_app.models import Parameter, Category, FormulaParameterCategory, ParameterData
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from passport_app.forms import ParameterDataForm
from django.http import HttpResponseRedirect

class ParameterDataUpdate(UpdateView):
    model = ParameterData
    fields = ['value','rate',]
    success_url = "/"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        pk_d = self.kwargs['pk_d']
        parameter = get_object_or_404(ParameterData, id=pk)
        form = ParameterDataForm(instance=parameter)
        html = render_to_string('passport/partial_modal_edit.html', {'form': form, 'id':parameter.id, 'id_d':pk_d}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        pk_d = self.kwargs['pk_d']
        super(ParameterDataUpdate, self).post(request, **kwargs)
        redir_str = "/details/?id=%i" % (pk_d)
        return redirect (redir_str)