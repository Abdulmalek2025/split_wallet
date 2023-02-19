from django import template

register = template.Library()

@register.filter
def user_amount(value,arg):
    value = float(value)
    arg = float(arg)
    if arg:return value * arg
    return ''