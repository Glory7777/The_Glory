from django import forms
from django.contrib.auth.hashers import check_password
from .models import SpUser


class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.'
        },
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )
    re_password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호 확인'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error("password", '비밀번호가 일치하지 않습니다.')
                self.add_error("re_password", '비밀번호가 일치하지 않습니다.')


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required': '올바른 이메일을 입력해주세요.'}, max_length=64, label='이메일')
    password = forms.CharField(error_messages={
                               'required': '비밀번호를 입력해주세요.'},  widget=forms.PasswordInput, label='비밀번호')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                spuser = SpUser.objects.get(email=email)
            except SpUser.DoesNotExist:
                self.add_error('email', "등록한 이메일이 없습니다. ")
                return  # 줄게 없으니까 리턴

            if not check_password(password, spuser.password):
                self.add_error("password", "비밀번호가 틀렸습니다.")
            # else: 여기서 할 수 없음
            #     self.user_id = shopuser.id


