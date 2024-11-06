from django import template

register = template.Library()

@register.filter(name='add')
def add(value, arg):
    """Add the arg to the value."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return value 