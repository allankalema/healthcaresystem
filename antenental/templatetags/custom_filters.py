from django import template

register = template.Library()

@register.filter(name='exclude_fields')
def exclude_fields(field_name, excluded_fields):
    """Check if a field name is in the excluded_fields list."""
    excluded_fields = excluded_fields.split(',')
    return field_name not in excluded_fields

@register.filter(name='add_class')
def add_class(value, arg):
    """Add a CSS class to a form field."""
    return value.as_widget(attrs={'class': arg})