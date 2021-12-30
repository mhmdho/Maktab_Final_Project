from django import forms
from .models import  Comment, Tag, Category, Post
from myuser.models import CustomUser
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['phone', 'username', 'email', 'password', 'confirm_password']

    def clean_confirm_new_password(self):
        password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_new_password']
        if password != confirm_password:
            raise ValidationError('Two new passwords must be equal!')
        
        return confirm_password


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password != confirm_new_password:
            raise ValidationError('Two new passwords must be equal!')
        
        return confirm_new_password


class AddCategoryForm(forms.Form):
    title = forms.CharField(max_length=255,min_length=3,
                           widget= forms.TextInput
                           (attrs={'placeholder':'Add new category here'}))
    def save(self):
        Category.objects.create(title=self.cleaned_data['title'])


class AddTagForm(forms.Form):
    title = forms.CharField(max_length=255,min_length=3,
                           widget= forms.TextInput
                           (attrs={'placeholder':'Add new tag here'}))
    def save(self):
        Tag.objects.create(title=self.cleaned_data['title'])


class CategoryDeleteForm(forms.ModelForm):
    class Meta : 
        model = Category
        fields = []


class EditCategoryForm(forms.ModelForm):
    title = forms.CharField(max_length=255,min_length=3,
                        widget= forms.TextInput
                        (attrs={'placeholder':'Add new name here'}))
    class Meta : 
        model = Category
        fields = ['title']


class TagDeleteForm(forms.ModelForm):
    class Meta : 
        model = Tag
        fields = []


class EditTagForm(forms.ModelForm):
    title = forms.CharField(max_length=255,min_length=3,
                        widget= forms.TextInput
                        (attrs={'placeholder':'Add new name here'}))
    class Meta : 
        model = Tag
        fields = ['title']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'like', 'supplier']


class PostDeleteForm(forms.ModelForm):
    class Meta : 
        model = Post
        fields = []


class EditPostForm(forms.ModelForm):
    class Meta : 
        model = Post
        exclude = ['slug', 'like', 'supplier']


class AddCommentForm(forms.ModelForm):
    title = forms.CharField(max_length=30,
                    widget= forms.TextInput
                    (attrs={'placeholder':'comment title'}))

    class Meta:
        model = Comment
        exclude = ['like', 'post', 'customer']


class ContactForm(forms.Form):
	name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)
