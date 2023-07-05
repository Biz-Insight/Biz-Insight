from django import template
from django.utils.safestring import SafeText

register = template.Library()


@register.filter
def div(value, arg):
    try:
        if isinstance(arg, SafeText):
            arg = float(arg)
        if isinstance(value, SafeText):
            value = float(value)
        result = value / arg
        return format(round(result, 1), ",")
    except (ValueError, ZeroDivisionError, TypeError):
        return None
