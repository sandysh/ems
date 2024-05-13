from django import forms

class UserForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=100,
        unique
        widget=forms.TextInput(
            attrs={
                'name': "first_name", 
                "placeholder": "Your first name", 
                "required": "",
                "class": "form-control"
                }
        ),
    # last_name = forms.CharField(
    #     label='Last Name',
    #     max_length=100,
    #     widget=forms.TextInput(
    #         attrs={
    #             'name': "last_name", 
    #             "placeholder": "Your last name", 
    #             "required": "",
    #             "class": "form-control"
    #             }
    #     ),
    # email = forms.CharField(
    #     label='Email',
    #     max_length=100,
    #     widget=forms.TextInput(
    #         attrs={
    #             'name': "email", 
    #             "placeholder": "Your email", 
    #             "required": "",
    #             "class": "form-control"
    #             }
    #     )
    )