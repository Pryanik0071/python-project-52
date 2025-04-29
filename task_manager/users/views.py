from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View

from .forms import UserForm, LoginForm
from task_manager.mixins import CustomLoginRequiredMixin, CustomCheckUserMixin


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users/index.html', context={
            'users': users,
        })


class CreateView(View):

    template = 'form.html'

    def get_context_data(self, form):
        return {'form': form,
                'title': _('Registration'),
                'button_text': _('Register')
                }

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, self.template, self.get_context_data(form))

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("User registered successfully"))
            form.save()
            return redirect('/login/')
        return render(request, self.template, self.get_context_data(form))


class UpdateView(CustomLoginRequiredMixin, CustomCheckUserMixin):

    template = 'form.html'

    def get_context_data(self, form, user):
        return {'form': form,
                'user': user,
                'title': _('Update user'),
                'button_text': _('Update')
                }

    def get_user(self):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(User, pk=user_id)

    def get(self, request, *args, **kwargs):
        user = self.get_user()
        form = UserForm(instance=user)
        return render(request, self.template, self.get_context_data(form, user))

    def post(self, request, *args, **kwargs):
        user = self.get_user()
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("User successfully changed"))
            form.save()
            return redirect('/users/')
        return render(request, self.template, self.get_context_data(form, user))


class DeleteView(CustomLoginRequiredMixin, CustomCheckUserMixin):

    template = 'users/delete.html'

    def get_user(self):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(User, pk=user_id)

    def get_context_data(self, user):
        return {
            'user': user,
            'title': _('Delete user'),
            'text': _('Are you sure you want to delete'),
            'button_text': _('Yes, delete')
        }

    def get(self, request, *args, **kwargs):
        user = self.get_user()
        return render(request, self.template, self.get_context_data(user))

    def post(self, request, *args, **kwargs):
        user = self.get_user()
        if user:
            user.delete()
            messages.success(request, _("User successfully deleted"))
        return redirect('/users/')


# Пользователь успешно удален
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
