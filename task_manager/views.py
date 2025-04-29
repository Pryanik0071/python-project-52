from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from .forms import LoginForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,
                                username=username,
                                password=password)
            if user is not None:
                messages.add_message(request,
                                     messages.SUCCESS, _("You are login"))
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None,
                               _("Please enter a valid username and password."
                                 " Both fields may be case sensitive."))
        return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.add_message(request,
                         messages.INFO, _("You are logout"))
    return redirect('/')
