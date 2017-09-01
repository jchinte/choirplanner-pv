from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter(name='iriPlus')
@stringfilter
def iriPlus(value):
    return value.replace(' ', '+')
