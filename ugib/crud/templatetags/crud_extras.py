from django import template

register = template.Library()

@register.filter
def addstr(arg1):
    arg1 = str(arg1)
    new_attr = arg1.replace(" ", "_")
    new_attr = new_attr.lower()
    return str(new_attr)