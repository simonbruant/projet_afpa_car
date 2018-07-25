from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import LoginForm, SignupForm, LogoutForm, PrivateDataCreateForm


# class SignupView(CreateView):
#     form_class = SignupForm
#     template_name = 'users/signup.html'
#     success_url = reverse_lazy('covoiturage:index')

def signup_view(request):
    signup_form = SignupForm(request.POST or None)
    private_data_form = PrivateDataCreateForm(request.POST or None)
    if signup_form.is_valid() and private_data_form.is_valid():
        user = signup_form.save()
        private_data = private_data_form.save(commit=False)
        private_data.user = user
        private_data.save()

        return redirect("covoiturage:index")

    return render(
        request, 
        'covoiturage/signup.html', 
        {   'signup_form': signup_form,
            'private_data_form': private_data_form,}
    )


class LoginView(FormView):
    form_class  = LoginForm
    template_name = 'covoiturage/index.html'
    success_url = reverse_lazy('covoiturage:dashboard')

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.GET.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('covoiturage:dashboard')
        print("pas valide")
        return super(LoginView, self).form_invalid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('covoiturage:dashboard')
        else:
            # Omit the form if you are not using it.
            form = self.form_class() 
            return render(request, self.template_name, {'form': form})

class LogoutView(LoginRequiredMixin, FormView):
    form_class = LogoutForm
    template_name = 'covoiturage/logout.html'

    def form_valid(self, form):
        logout(self.request)
        return HttpResponseRedirect(reverse('covoiturage:index'))


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            print('form valide')
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('covoiturage:dashboard')

    else: 
        form = PasswordChangeForm(user=request.user)

    context = {'form': form }
    return render(request, 'covoiturage/profil/password.html', context)