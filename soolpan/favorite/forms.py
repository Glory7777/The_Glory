from django import forms


class FavoriteForm(forms.Form):
    # request 추가적인 인자를 가질 수 있도록 초기화 설정
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # 위젯 숨기기
    like = forms.IntegerField(
        error_messages={'required': '수량을 입력해 주세요.'}, label='좋아요', widget=forms.HiddenInput)
    # 위젯 숨기기 , widget=forms.HiddenInput
    post = forms.IntegerField(
        error_messages={'required': '상품정보를 입력해주세요.'}, label='술정보', widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super().clean()
        like = cleaned_data.get('like')
        post = cleaned_data.get('post')
