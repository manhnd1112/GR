from django import template
register = template.Library()

@register.filter
def get_item(List, i):
    return List[int(i)]