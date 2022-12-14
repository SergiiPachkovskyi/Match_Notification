from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from sub.models import Subscription


class UserLoginForm(AuthenticationForm):
    """A class to represent a Login form."""
    username = forms.CharField(label="Ім'я користувача", widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):
    """A class to represent a Register form."""
    username = forms.CharField(label="Ім'я користувача", widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Підтвердження пароля",
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SubscriptionForm(forms.ModelForm):
    """A class to represent a Subscription form."""
    team_name = forms.CharField(label="Назва команди", widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user', None)
        super(SubscriptionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        art = super().save(commit=False)
        art.user = self.current_user
        if commit:
            art.save()
            self.save_m2m()
        return art

    class Meta:
        model = Subscription
        fields = ['team_name']
