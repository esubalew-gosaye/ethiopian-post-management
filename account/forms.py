from .models import *
from django.forms import *
from django import forms


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "middle_name", "last_name", "email", "password", "sex", "address", "phone"]

        GENDER = (
            ("is_hidden", "Select Gender"),
            ('F', "FEMALE"),
            ('M', 'Male'),
            ('O', 'Other')
        )

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Middle Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "sex": forms.Select(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "phone number"})
        }