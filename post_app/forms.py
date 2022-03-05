from django import forms
from django.forms import ModelForm
from .models import *


class ImageUploadForm(forms.Form):
    title = forms.CharField(max_length=20)
    caption = forms.CharField(max_length=150)
    image = forms.ImageField()


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['track_id', 'date_send', 'date_modified', 'postman', 'seen']

        widgets = {
            "sender": forms.Select(attrs={"class": "form-control"}),
            "receiver": forms.Select(attrs={"class": "form-control"}),
            "post_box_num": forms.TextInput(attrs={"class": "form-control", "placeholder": "Post Box number"}),
            "sender_full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sender Full Name"}),
            "sender_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sender Phone"}),
            "sender_address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sender Address"}),
            "rec_full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Receiver Full Name"}),
            "rec_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Receiver Phone"}),
            "rec_address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Receiver Address"}),
            'post_location': forms.TextInput(attrs={"class": "form-control", "placeholder": "Post Office Location"}),
        }
