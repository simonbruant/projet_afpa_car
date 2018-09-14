from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView

from calendar import day_abbr
from carpooling.forms import DefaultTripFormSet
from carpooling.models import DefaultTrip, Trip

settings.app_static_url = 'carpooling/app'

class DefaultTripView(View):
    template_name = 'carpooling/calendar.html'

    def get(self, request):
        user = self.request.user
        formset = DefaultTripFormSet(queryset=DefaultTrip.objects.filter(
            user=user), form_kwargs={'user': user},)
        day_label = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        context = {
            'trips': user.default_trips.all(),
            'formset': formset,
            'day_label': day_label,
            'calendar_url' : '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_CALENDAR_FILE)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = self.request.user
        formset = DefaultTripFormSet(request.POST, queryset=DefaultTrip.objects.filter(user=user), 
                                    form_kwargs={'user': user})
        for i, form in enumerate(formset.forms):
            if form.is_valid():
                default_trip = form.save(commit=False)
                default_trip.user = user
                default_trip.has_for_destination = user.user_profile.afpa_center.address

                is_form_valid = (not form.cleaned_data.get('morning_departure_time') 
                                or not form.cleaned_data.get('morning_arriving_time')
                                or not form.cleaned_data.get('evening_departure_time')
                                or not form.cleaned_data.get('has_for_start')
                                or form.cleaned_data.get('deactivate'))

                if is_form_valid:
                    default_trip.has_for_start = None
                    default_trip.morning_departure_time = None
                    default_trip.morning_arriving_time = None
                    default_trip.evening_departure_time = None
                    default_trip.deactivate = True

                default_trip.day = default_trip._meta.get_field('day').choices[i][1]
                default_trip.save()

        return redirect('carpooling:calendar')
        
class TripView(View):
    template_name = 'carpooling/trip.html'

    def get(self, request):
        city_search = request.GET.get('city')
        day_search = request.GET.get('day')
        user = request.user
        visible_trips = []
        user_trips = [trip for trip in user.default_trips.all() if not trip.deactivate]
        if not city_search and not day_search:
            all_trips = DefaultTrip.objects.all().exclude(user=user)            
        else:
            all_trips = DefaultTrip.objects.filter(has_for_start__city__startswith=city_search,
                                                    day__startswith=day_search).exclude(user=user)
            if day_search:
                user_trips = user.default_trips.all()

        for trip in all_trips:
            for user_trip in user_trips:
                if user_trip.day == trip.day:
                    if user_trip.user_is_driver or (not user_trip.user_is_driver and trip.user_is_driver):
                        visible_trips.append(trip)

        return render(request, 'carpooling/trip.html', {'trips': visible_trips})

class TripDetailView(DetailView):
    model = DefaultTrip
    template_name = 'carpooling/trip.html'

    def get(self, request, pk) :
        trip = get_object_or_404(DefaultTrip, pk=pk)
        return render(request, 'carpooling/trip_detail.html', {'trip': trip})

class PropositionView(DetailView):
    model = DefaultTrip
    template_name = 'carpooling/proposition.html'
    context_object_name = 'trip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_default_trips'] = self.request.user.default_trips.all()
        return context