from django import forms


class ImageUploadForm(forms.Form):
    title = forms.CharField(max_length=20)
    caption = forms.CharField(max_length=150)
    image = forms.ImageField()
