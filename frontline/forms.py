from django import forms
from .models import Entry, ImageEntry


class RichtextForm(forms.ModelForm):
    name = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Entry


class ImageUploadForm(forms.ModelForm):
    name = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = ImageEntry