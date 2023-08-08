from django import forms
from .models import Tal, Comment

class DetailForm(forms.ModelForm):
    class Meta:
        model = Tal
        fields = ['name']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body', 'color', 'flavor', 'sweet', 'sour', 'carbon', 'total']
        widgets = {
        'color': forms.RadioSelect,
        'flavor': forms.RadioSelect,
        'sweet': forms.RadioSelect,
        'sour': forms.RadioSelect,
        'carbon': forms.RadioSelect,
        'total': forms.RadioSelect,
        }
        