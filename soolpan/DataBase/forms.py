from django import forms
from .models import Tal

class DetailForm(forms.ModelForm):
    class Meta:
        model = Tal
        fields = ['name']
