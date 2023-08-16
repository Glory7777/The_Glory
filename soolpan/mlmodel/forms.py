from django import forms

class InputForm(forms.Form):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        # Add more choices as needed
    )

    input_0 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="색")
    input_1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="탄산감")
    input_2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="향")
    input_3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="산미")
    input_4 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="당도")