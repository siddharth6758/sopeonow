from django import template
register = template.Library()

@register.filter
def dict_lookup(dict_obj, key):
    return dict_obj.get(key, None)