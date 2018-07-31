from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm

from django.forms import TextInput, PasswordInput

from .models import User, PrivateData

class SignupForm(forms.ModelForm):
    password1   = forms.CharField(label="Password",  widget=PasswordInput(attrs={'class': 'form-control'})) # ini == password
    password2   = forms.CharField(label='Confirm password', widget=PasswordInput(attrs={'class': 'form-control'}))

    username    = forms.RegexField(label='Username',
                                    min_length=3,
                                    regex=r'^[\w._-]+$',  
                                    error_messages = {'invalid': "This value may contain only" 
                                    "letters, numbers and ./-/_ characters."},
                                    widget=TextInput(attrs={'class': 'form-control'}) )

 

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
        }

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
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # save the provided password in hashed format
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print(self.cleaned_data["username"])
        user.username = self.cleaned_data["username"]
        # user.is_active = False # send confirmation email via signals
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',)
    password = forms.CharField(widget=forms.PasswordInput)

class LogoutForm(forms.Form):
    pass

class PrivateDataCreateForm(forms.ModelForm):
    class Meta:
        model = PrivateData
        fields = ('phone_number', 'afpa_number',)
        widgets = {
            'phone_number': TextInput(attrs={'class': 'form-control'}),
            'afpa_number': TextInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        widgets = {
            'old_password': PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': PasswordInput(attrs={'class': 'form-control'}),
            
        }
#################################################################
    
class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'is_active', 'is_staff', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name', 'avatar', 'is_active', 'is_staff', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


