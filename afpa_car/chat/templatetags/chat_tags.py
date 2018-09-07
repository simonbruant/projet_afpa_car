import datetime

from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def choose_username(object, user):
    if user != object.first:
        return object.first.username
    return object.second.username

@register.filter
def choose_photo(object, user):
    if user != object.first:
        return object.first.user_profile.profile_image.url
    return object.second.user_profile.profile_image.url

@register.filter
def date_format(date):
    date = date
    today = timezone.now()
    months = ['Janv.', 'Févr.', 'Mars', 'Avr.', 'Mai', 'Juin', 'Juil.', 
                'Août', 'Sept.', 'Oct.', 'Nov.', 'Déc.'] 
    days = ['Lun.', 'Mar.', 'Mer.', 'Jeu.', 'Ven.', 'Sam.', 'Dim.']


    if not date:
        return ""

    elif date.year != today.year:
        return "{} {} {}".format(date.day, months[date.month - 1], date.year)

    elif (today.day - date.day) > 6:
        return "{} {}".format(date.day, months[date.month - 1])

    else:
        if date.day != today.day:
            if today.day - date.day == 1:
                return "Hier"
            return days[date.weekday()]
        return "{} h {}".format(date.hour, date.minute)

    return date
