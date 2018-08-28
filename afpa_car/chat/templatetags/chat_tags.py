from django import template
register = template.Library()

@register.filter
def choose_username(object, user):
    if user != object.first:
        return object.first.username
    return object.second.username

@register.filter
def choose_photo(object, user):
    if user != object.first:
        return object.first.user_profile.profile_image
    return object.second.user_profile.profile_image
    
@register.filter
def choose_photo_display(object, user):
    if user != object.first:
        return object.first.user_profile.profile_image.url
    return object.second.user_profile.profile_image.url

