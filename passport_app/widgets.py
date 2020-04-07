import json

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class NodeInputWidget(forms.widgets.FileInput):
    template_name = 'forms/widgets/node_input.html'

    def __init__(self, attrs=None, options={}):
        self.options = options

        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(render_to_string(self.template_name,
                                          context))