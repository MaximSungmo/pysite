from django import forms


class PhotoForm(forms.Form):
    file = forms.FileField()
    image = forms.ImageField()