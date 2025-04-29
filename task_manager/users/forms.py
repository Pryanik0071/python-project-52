from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


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

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if the username already exists, excluding the current user
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This username is already taken.")
        return username
