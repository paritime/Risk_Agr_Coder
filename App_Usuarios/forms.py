from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombres = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "nombres", "apellidos", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["nombres"]
        user.last_name = self.cleaned_data["apellidos"]
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    nombres = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=30)
    password1 = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(
        label="Confirmar contraseña", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ("username", "nombres", "apellidos",
                  "email", 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserChangeForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["nombres"]
        user.last_name = self.cleaned_data["apellidos"]
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 == password2:
            user.set_password(password1)

        if commit:
            user.save()
        return user
