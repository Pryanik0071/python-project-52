from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150, required=True, label=_("First name")
    )
    last_name = forms.CharField(
        max_length=150, required=True, label=_("Last name")
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1', 'password2'
                  )


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
