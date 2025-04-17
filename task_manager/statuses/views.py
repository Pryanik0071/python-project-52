from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from .models import Status
from .forms import StatusForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'statuses/index.html', context={
            'statuses': statuses,
        })


class CreateView(View):

    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'statuses/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            messages.success(request, "Статус успешно создан")
            form.save()
            return redirect('/statuses/')
        return render(request, 'statuses/create.html', {'form': form})


class UpdateView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        status = Status.objects.get(id=pk)
        form = StatusForm(instance=status)
        return render(request, 'statuses/update.html', {'form': form, 'pk': pk})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        status = Status.objects.get(id=pk)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            messages.success(request, "Статус успешно изменен")
            form.save()
            return redirect('/statuses/')
        return render(request, 'statuses/update.html', {'form': form, 'pk': pk})


class DeleteView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            status = Status.objects.get(id=pk)
        except Status.DoesNotExist:
            raise Http404
        form = StatusForm(instance=status)
        return render(request, 'statuses/delete.html', {'form': form,
                                                        'name': status.name,
                                                        'pk': pk})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        status = Status.objects.get(id=pk)
        if status:
            status.delete()
            messages.success(request, "Статус успешно удален")
        return redirect('/statuses/')
