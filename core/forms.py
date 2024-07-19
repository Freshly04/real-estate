from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "enter username",
        "class": "form control"
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "enter email",
        "class": "form control"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "enter password",
        "class": "form control"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "enter password",
        "class": "form control"
    }))


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "enter username",
        "class": "form control"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "enter password",
        "class": "form control"
    }))


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "price", "description", "is_sold", "stock", "image"]


class ProductRegisterForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = ["category", "name", "price", "description", "is_sold", "stock", "image"]
