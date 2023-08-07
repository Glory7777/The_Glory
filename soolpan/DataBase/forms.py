from django import forms
from .models import Tal, Comment

class DetailForm(forms.ModelForm):
    class Meta:
        model = Tal
        fields = ['name']


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','body']
        