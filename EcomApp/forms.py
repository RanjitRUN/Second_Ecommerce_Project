from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm, 
                                    AuthenticationForm, 
                                    UsernameField, PasswordChangeForm, PasswordResetForm,
                                    SetPasswordForm)
from django.utils.translation import gettext_lazy as _, gettext
from django.contrib.auth import password_validation
from .models import Customer



class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label=('Password'), max_length=30, required=True, 
                                widget=forms.PasswordInput( attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=('Confirm Password'), max_length=30, required=True, 
                                widget=forms.PasswordInput( attrs={'class': 'form-control'}))
    email =  forms.EmailField(label=('Email'), required=True, 
                                widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        label = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}



class LoginForm(AuthenticationForm):
    username = UsernameField(label=('username'), widget=forms.TextInput( attrs={'class': 'form-control', 
                                                                                      'autofocus': True}))
    password = forms.CharField(label=_('password'), strip=False, widget=forms.PasswordInput( attrs={'class': 'form-control', 
                                                                                      'autocomplete': 'current-password'}))
   
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, max_length=30, required=True, 
                                widget=forms.PasswordInput( attrs={'class': 'form-control',
                                                                   'autocomplete':'current-password',
                                                                   'autofocus':True}))
    new_password1 = forms.CharField(label=_('New Password'), strip=False, max_length=30, required=True, 
                                widget=forms.PasswordInput( attrs={'class': 'form-control',
                                                                   'autocomplete':'current-password'}),
                                                                   help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm Password'), strip=False, max_length=30, required=True, 
                                widget=forms.PasswordInput( attrs={'class': 'form-control',
                                                                   'autocomplete':'current-password'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_('Email'), required=True, 
                                widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
class MySetpasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality','city', 'state', 'zipcode']
        widgets = {
                    'name':forms.TextInput(attrs={'class': 'form-control'}),
                    'locality':forms.TextInput(attrs={'class': 'form-control'}),
                    'city': forms.TextInput(attrs={'class': 'form-control'}),
                    'state': forms.Select(attrs={'class': 'form-control'}),
                    'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
                  }
        
