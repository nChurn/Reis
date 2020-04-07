from django import template
register = template.Library()

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)

@register.filter
def replace_space(value):
    return value.replace(" ","_")
    
@register.simple_tag
def update_variable(value):
    data = value
    return data