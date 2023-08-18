from django import forms
from .models import Tal, Comment

class DetailForm(forms.ModelForm):
    class Meta:
        model = Tal
        fields = ['name']


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['body', 'color', 'flavor', 'sweet', 'sour', 'carbon', 'total']
        widgets = {
        'color': forms.RadioSelect,
        'flavor': forms.RadioSelect,
        'sweet': forms.RadioSelect,
        'sour': forms.RadioSelect,
        'carbon': forms.RadioSelect,
        'total': forms.RadioSelect,
        }

class UserInputForm(forms.Form):
    user_input = forms.CharField(label='검색어', widget=forms.TextInput(attrs={'placeholder': '검색하고 싶은 술 이름을 입력해주세요.'}))