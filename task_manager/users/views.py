from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.models import User
from task_manager.users.forms import UserForm


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
            form.save()
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
