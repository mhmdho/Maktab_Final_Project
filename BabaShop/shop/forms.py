from django.forms import ModelForm, Textarea, TextInput
from django.forms.fields import ChoiceField
from django.forms.widgets import CheckboxSelectMultiple, ClearableFileInput, NumberInput, RadioSelect, Select, SelectMultiple
from .models import Product, Shop


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


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'created_at', 'updated_at', 'shop', 'is_confirmed']
        widgets = {
            'name': TextInput(attrs={'class':'form-control', 
                                    'placeholder': "Enter your product's name"}),

            'price': NumberInput(attrs={'class':'form-control', 
                                    'placeholder': '10.99 ($)'}),

            'discount': NumberInput(attrs={'class':'form-control', 
                                    'placeholder': 'Enter like: 0.15  - It is equal to 15%'}),

            'stock': NumberInput(attrs={'class':'form-control', 
                                    'placeholder': '0'}),

            'weight': NumberInput(attrs={'class':'form-control', 
                                    'placeholder': '450 (gr)'}),

            'description': TextInput(attrs={'class':'form-control', 
                                    'placeholder': ""}),

            'category': Select(attrs={'class':'form-control', 
                                    'placeholder': ""}),

            'tag': SelectMultiple(attrs={'class':'form-control', 
                                    'placeholder': "choose"}),

            'image': ClearableFileInput(attrs={'class':'form-control-file'}),

            'is_active': RadioSelect(attrs={'class':'form-check-input'}),
        }