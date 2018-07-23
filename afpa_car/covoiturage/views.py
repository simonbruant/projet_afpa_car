from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/dashboard.html'

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'covoiturage/calendar.html'

    