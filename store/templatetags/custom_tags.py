from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''

@register.filter
def right_side(value, arg):
    try:
        return ' '.join(value.split(' ')[arg:])
    except (ValueError, TypeError):
        return ''