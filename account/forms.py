from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from django.forms.widgets import TextInput, PasswordInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    # Email Validation

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")

        if len(email) >= 350:
            raise forms.ValidationError("Email must have less than 350 characters")

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User

        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already registered")

        if len(email) >= 350:
            raise forms.ValidationError("Email must have less than 350 characters")

        return email
