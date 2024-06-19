from django import forms
from django.contrib.auth.models import User
from store.models import Application


#now forms from account_app are used
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data

        password = cd['password']
        password2 = cd['password2']

        if password != password2:
            raise forms.ValidationError('Passwords must match')

        return password2


class ApplicationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__name', 'placeholder': 'Имя'}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__tel', 'placeholder': 'Номер телефона'}))

    class Meta:
        model = Application
        fields = ['name', 'phone_number']
