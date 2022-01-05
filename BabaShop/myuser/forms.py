from django.forms import TextInput
from django.forms.widgets import EmailInput
from .models import CustomUser

from django.contrib.auth.forms import UserCreationForm




class SupplierRegisterForm(UserCreationForm):
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

            'password1': TextInput(attrs={'class':'form-control', 
                                    'placeholder': 'Password'}),

            'password2': TextInput(attrs={'class':'form-control', 
                                    'placeholder': 'Confirm Password'}),
        }

    def save(self, commit=True):
        user = super(SupplierRegisterForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
