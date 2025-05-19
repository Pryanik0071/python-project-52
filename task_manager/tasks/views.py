from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import Task
from .forms import TaskForm
from task_manager.mixins import CustomLoginRequiredMixin


class BaseTaskView(CustomLoginRequiredMixin):
    def get_task(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=pk)


class IndexView(CustomLoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(request, 'tasks/index.html', {'tasks': tasks})


class CreateView(CustomLoginRequiredMixin):

    template = 'form.html'

    def get_context_data(self, form):
        return {'form': form,
                'title': _('Create task'),
                'button_text': _('Create')
                }

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, self.template, self.get_context_data(form))

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Task created successfully"))
            return redirect('/tasks/')
        return render(request, self.template, self.get_context_data(form))


class UpdateView(BaseTaskView):

    template = 'form.html'

    def get_context_data(self, form, obj):
        return {'form': form,
                'obj': obj,
                'title': _('Update task'),
                'button_text': _('Update')
                }

    def get(self, request, *args, **kwargs):
        task = self.get_task()
        form = TaskForm(instance=task)
        return render(request, self.template, self.get_context_data(form, task))

    def post(self, request, *args, **kwargs):
        task = self.get_task()
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Task successfully changed"))
            form.save()
            return redirect('/tasks/')
        return render(request, self.template, self.get_context_data(form, task))


class DeleteView(BaseTaskView):

    def get_context_data(self, obj):
        return {
            'obj': obj,
            'title': _('Delete task'),
            'text': _('Are you sure you want to delete'),
            'button_text': _('Yes, delete')
        }

    def get(self, request, *args, **kwargs):
        task = self.get_task()
        if task.author != self.request.user:
            messages.error(request, _("Only the author can delete the task"))
            return redirect('/tasks/')
        return render(request, 'tasks/delete.html', self.get_context_data(task))

    def post(self, request, *args, **kwargs):
        task = self.get_task()
        if task:
            task.delete()
            messages.success(request, _("Task successfully deleted"))
        return redirect('/tasks/')
