from django.forms import ModelForm, Textarea, TextInput
from django.forms.fields import ChoiceField
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from .models import Shop


class CreateShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'address', 'type')
        widgets = {
            'name': TextInput(attrs={'class':'form-control', 
                                    'placeholder': "Enter your shop's name"}),

            'address': TextInput(attrs={'class':'form-control', 
                                    'placeholder': 'No.12, Jordan st., Tehran'}),
            'type': RadioSelect(attrs={'class':'form-check-input position-relative'}),
        }