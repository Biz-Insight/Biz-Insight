from django import template
from django.utils.safestring import SafeText
from itertools import zip_longest
import math

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


@register.filter
def zip_lists(a, b):
    return zip_longest(a, b)


@register.filter(name="is_nan")
def is_nan(value):
    return math.isnan(value)
