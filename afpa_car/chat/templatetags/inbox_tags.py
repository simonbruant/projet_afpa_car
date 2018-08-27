from django import template
register = template.Library()

@register.filter
def choose(object, user):
    if user != object.first:
        return object.first.username

    return object.second.username

