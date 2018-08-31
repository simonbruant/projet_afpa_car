from django import forms
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (ReadOnlyPasswordHashField, PasswordChangeForm as BasePasswordChangeForm, 
                                        PasswordResetForm as BasePasswordResetForm, 
                                        SetPasswordForm as BaseSetPasswordForm)
from django.forms import TextInput, PasswordInput, EmailInput

from .models import User, PrivateData
from carpooling.models import AfpaCenter


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_admin')
        widgets = {
            'email': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'email': "Adresse Email",
            'first_name': "Prénom",
            'last_name': "Nom de famille",
        }

    password1   = forms.CharField(label="Mot de Passe",  widget=PasswordInput(attrs={'class': 'form-control'}))
    password2   = forms.CharField(label='Confirmation Mot de Passe', widget=PasswordInput(attrs={'class': 'form-control'}))
    username    = forms.RegexField(regex=r'^[\w._-]+$', label='Pseudonyme',
                                    min_length=3,
                                    error_messages = {'invalid': "Votre ne pseudonyme ne peut contenir que des lettres,"
                                    "nombres ou caractères suivants : ./_/-"},
                                    widget=TextInput(attrs={'class': 'form-control'}) )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = User.objects.filter(email=email)
        if user.count():
            raise ValidationError("Cette adresse email est déjà utilisée sur le site")
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        user = User.objects.filter(username=username)
        if user.count():
            raise ValidationError("Pseudonyme existant")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class SignupForm(UserCreationForm):
    phone_number = forms.RegexField(regex=r'^[0+][\d]+$',label="Numéro de téléphone",
                                    min_length=10, max_length=13, 
                                    error_messages={'invalid': 'Numéro de téléphone invalide'}, 
                                    widget=TextInput(attrs={'class': 'form-control'}))
    afpa_number = forms.RegexField(regex=r'^\d+$', label="Identifiant Afpa",
                                    min_length=8, max_length=8,
                                    error_messages={'invalid': 'Le numéro AFPA est composé uniquement de nombres'}, 
                                    widget=TextInput(attrs={'class': 'form-control'}))
    afpa_center = forms.ModelChoiceField(queryset=AfpaCenter.objects.all(), label='Centre AFPA',
                                        widget=forms.Select(attrs={'class': 'custom-select'}))

    class Meta(UserCreationForm.Meta):
        exclude = ('is_active', 'is_admin', 'is_staff')



class LoginForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(attrs={'class':'form-control mb-3','placeholder': 'Adresse Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control mb-3','placeholder': 'Mot de Passe'}))

    def __init__(self, request, *args, **kwargs):
        # do not pass 'request' to the parent
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if email is not None and password:
            self.user = authenticate(username=email, password=password)
            if not self.user:
                raise forms.ValidationError("Vos identifiants ne correspondent pas")
            elif not self.user.is_active:
                raise forms.ValidationError("Veuillez confirmez votre adresse email")
        return self.cleaned_data

    def get_user(self):
        return self.user

class LogoutForm(forms.Form):
    pass

class SetPasswordForm(BaseSetPasswordForm):
    error_messages = {
            'password_mismatch': 'Les deux mots de passes ne sont pas identiques',
    }

    new_password1 = forms.CharField(
        label="Nouveau Mot de Passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control require-input'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control require-input'}),
    )

class PasswordChangeForm(SetPasswordForm, BasePasswordChangeForm, ):
    error_messages = {
            'password_incorrect': 'Ancien Mot de Passe incorrect',
    }

    old_password = forms.CharField(
        label="Ancien Mot de Passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control require-input', 'autofocus': True}),
    )

class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=TextInput(attrs={'class': 'form-control'}))

class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        fields = ('password', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_admin')

    username   = forms.RegexField(regex=r'^[\w._-]+$', label='Pseudonyme',
                                    min_length=3,
                                    error_messages = {'invalid': "Votre ne pseudonyme ne peut contenir que des lettres,"
                                    "nombres ou caractères suivants : ./_/-"},
                                    widget=TextInput(attrs={'class': 'form-control'}) )

    def clean_password(self):
        return self.initial["password"]


