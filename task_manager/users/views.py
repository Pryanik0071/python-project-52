from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from .forms import UserForm, LoginForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users/index.html', context={
            'users': users,
        })


class UserCreateView(View):

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('/')


class UserUpdateView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        form = UserForm(instance=user)
        return render(request, 'users/update.html', {'form': form, 'user_id': user_id})

    # def post(self, request, *args, **kwargs):
    #     form = UserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     return redirect('/')

    # def get(self, request, *args, **kwargs):
    #     category_id = kwargs.get('id')
    #     category = Category.objects.get(id=category_id)
    #     form = CategoryForm(instance=category)
    #     return render(request, 'categories/update.html', {'form': form, 'category_id': category_id})


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
                login(request, user)
                messages.add_message(request,
                                     messages.SUCCESS, _("You are login"))
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
    # Redirect to a success page.
