from django import forms

class ConnexionForm(forms.Form):
    username = forms.CharField(label="username", max_length=30)
    password = forms.CharField(label="password", widget=forms.PasswordInput)