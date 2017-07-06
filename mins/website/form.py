from django import forms


# class LoginForm(forms.Form):
#         username = forms.CharField()
#         password = forms.CharField()

class UserForm(forms.Form):
        user_upload_file = forms.FileField()

