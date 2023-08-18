from django import forms

class UserInputForm(forms.Form):
    user_input = forms.CharField(label='검색어', widget=forms.TextInput(attrs={'placeholder': '검색하고 싶은 술 이름을 입력해주세요.'}))