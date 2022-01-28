from django import forms
from django.forms import ModelForm, TextInput
from django.forms import Form
from django.forms.widgets import EmailInput
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class SupplierRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Password',
                                        'autocomplete': 'new-password',
                                        'class':'form-control',
                                        'id': "password-field",
                                        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
                                        'autocomplete': 'new-password',
                                        'class':'form-control',
                                        'id': "password-field2",
                                        'placeholder': 'Confirm Password',
                                        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = CustomUser
        fields = ("phone", "username", "email", "password1", "password2")
        widgets = {
            'phone': TextInput(attrs={'class':'form-control', 
                                    'placeholder': "Phone"}),

            'username': TextInput(attrs={'class':'form-control', 
                                    'placeholder': 'Username'}),
        
            'email': EmailInput(attrs={'class':'form-control', 
                                    'placeholder': 'E-mail'}),
        }

    def save(self, commit=True):
        user = super(SupplierRegisterForm, self).save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.is_supplier = True
        if commit:
            user.save()
        return user


class SupplierLoginForm(Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "Phone or Username or Email",
            'class':'form-control',           
            'autofocus': True}))
    
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class':'form-control', 
            'id': "password-field",
            'autocomplete': 'current-password'}),
    )


class SupplierPhoneVerifyForm(Form):
    otp = forms.CharField(
        max_length=6, 
        min_length=6,
        widget=forms.TextInput(
            attrs={
            'placeholder': 'Enter the code',
            'class':'form-control text-center'}),
    )


class SupplierLoginOtpForm(Form):
    otp = forms.CharField(
        max_length=6, 
        min_length=6,
        widget=forms.TextInput(
            attrs={
            'placeholder': 'Enter The Code',
            'class':'form-control'}))
    
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                'id': 'login_phone',
                'placeholder': "Registered Phone"}))
