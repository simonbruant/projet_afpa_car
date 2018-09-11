from django import template
register = template.Library()

@register.filter
def index(list, i):
    return list[int(i)]

@register.filter
def is_deactivate(trips):
    for trip in trips:
        if not trip.deactivate:
            return True
    return False