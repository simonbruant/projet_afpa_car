from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, TemplateView, UpdateView, DeleteView

from carpooling.forms import DefaultTripFormSet, PropositionForm, PropositionUpdateForm
from carpooling.models import DefaultTrip, Trip, Proposition, Register

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
        context = {
            'trip': trip,
            'map_trip_url': '{}/{}'.format(settings.app_static_url, settings.CARPOOLING_MAP_TRIP_FILE),
            'user_default_trips': self.request.user.default_trips.all()
        }
        return render(request, 'carpooling/trip_detail.html', context)

class PropositionView(FormView):
    template_name = 'carpooling/proposition/proposition.html'
    form_class = PropositionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = get_object_or_404(DefaultTrip, pk=self.kwargs['pk'])
        context ['trip'] = trip
        return context

    def form_valid(self, form, **kwargs):
        first_user = self.request.user
        proposition = form.save(commit=False)
        proposition.first_user = first_user
        trip = get_object_or_404(DefaultTrip, pk=self.kwargs['pk'])
        second_user = trip.user
        proposition.default_trip = trip
        proposition.second_user = second_user
        proposition.save()
        return render(self.request, 'carpooling/proposition/proposition_send.html')

class PropositionUpdateView(UpdateView):
    model = Proposition
    template_name = 'carpooling/proposition/proposition_detail.html'
    form_class =  PropositionUpdateForm
    success_url = reverse_lazy('carpooling:dashboard')

    def form_valid(self, form, **kwargs):
        proposition = form.save(commit=False)
        if proposition.default_trip.user == self.request.user :
            user = proposition.first_user
        else:
            user = proposition.second_user
            
        trip = proposition.default_trip
        register = Register()
        register.trip = trip
        register.user = user
        register.save()
        proposition.delete()
        return HttpResponseRedirect(self.get_success_url())
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposition = self.get_object()
        context ['trip'] =  proposition.default_trip
        return context
        

class CounterPropositionView(FormView):
    template_name = 'carpooling/proposition/proposition_counter.html'
    form_class = PropositionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposition = get_object_or_404(Proposition, pk=self.kwargs['pk']) 
        context ['proposition'] = proposition
        return context

    def form_valid(self, form, **kwargs):
        first_user = self.request.user
        counter_proposition = form.save(commit=False)
        counter_proposition.first_user = first_user
        proposition = get_object_or_404(Proposition, pk=self.kwargs['pk'])

        second_user = proposition.first_user
        counter_proposition.default_trip = proposition.default_trip
        counter_proposition.second_user = second_user
        counter_proposition.save()
        proposition.delete()
        return render(self.request, 'carpooling/proposition/proposition_send.html')
    
class PropositionRefusedView(DeleteView):
    model = Proposition
    template_name = 'carpooling/proposition/proposition_refused.html'
    success_url = reverse_lazy('carpooling:dashboard')


