from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placerholder': 'Usuario',
                                                             'class': 'login__input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placerholder': 'Contraseña',
                                                                 'class': 'login__input'}))