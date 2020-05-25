from django import template
register = template.Library()

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)

@register.filter
def category_sort_by_point(queryset):
    return queryset.extra(select={'int_point': "CAST(replace(point, '.', '') AS INTEGER)"}). \
            order_by('int_point')

@register.filter
def replace_space(value):
    return value.replace(" ","_")
    
@register.simple_tag
def update_variable(value):
    data = value
    return data