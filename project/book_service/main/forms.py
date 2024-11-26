from django import forms
from django.db import connection

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=50, label='Имя пользователя')
    email = forms.EmailField(max_length=100, label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    is_superuser = forms.BooleanField(required=False, label='Суперадминистратор')

    def clean_username(self):
        username = self.cleaned_data['username']
        # Проверяем, существует ли уже пользователь с таким именем
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # Проверяем, существует ли уже пользователь с таким email
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", [email])
            if cursor.fetchone()[0] > 0:
                raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email