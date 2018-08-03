from django import forms
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (ReadOnlyPasswordHashField, PasswordChangeForm as BasePasswordChangeForm, 
                                        PasswordResetForm as BasePasswordResetForm, 
                                        SetPasswordForm as BaseSetPasswordForm)
from django.forms import TextInput, PasswordInput

from .models import User, PrivateData

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')
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
    username    = forms.RegexField(label='Pseudonyme',
                                    min_length=3,
                                    regex=r'^[\w._-]+$',  
                                    error_messages = {'invalid': "Votre ne pseudonyme ne peut contenir que des lettres,"
                                    "nombres ou caractères suivants : ./_/-"},
                                    widget=TextInput(attrs={'class': 'form-control'}) )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.is_active = False # send confirmation email via signals
        if commit:
            user.save()
        return user

class PrivateDataCreateForm(forms.ModelForm):
    class Meta:
        model = PrivateData
        fields = ('phone_number', 'afpa_number')
    
    phone_number = forms.RegexField(regex=r'^[0+][\d]+$',label="Numéro de téléphone",
                                    min_length=10, max_length=13, 
                                    error_messages={'invalid': 'Numéro de téléphone invalide'}, 
                                    widget=TextInput(attrs={'class': 'form-control'}))
    afpa_number = forms.RegexField(regex=r'^\d+$', label="Identifiant Afpa",
                                    min_length=8, max_length=8,
                                    error_messages={'invalid': 'Le numéro AFPA est composé uniquement de nombres'}, 
                                    widget=TextInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    email = forms.EmailField(widget=TextInput(attrs={'class':'form-control mb-3','placeholder': 'Adresse Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control mb-3','placeholder': 'Mot de Passe'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Vos identifiants ne correspondent pas")
        return self.cleaned_data

class LogoutForm(forms.Form):
    pass

class PasswordChangeForm(BasePasswordChangeForm):
    error_messages = {
            'password_mismatch': 'Les deux mots de passes ne sont pas identiques',
            'password_incorrect': 'Ancien Mot de Passe incorrect',
        }

    new_password1 = forms.CharField(
        label="Nouveau Mot de Passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    old_password = forms.CharField(
        label="Ancien Mot de Passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autofocus': True}),
    )

class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=TextInput(attrs={'class': 'form-control'}))

class SetPasswordForm(BaseSetPasswordForm):
    new_password1 = forms.CharField(
        label="Nouveau Mot de Passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

#################################################################
    
class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'is_active', 'is_staff', 'is_admin')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


