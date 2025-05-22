from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import Status
from .forms import StatusForm
from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.tasks.models import Task


class IndexView(CustomLoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'statuses/index.html', {'statuses': statuses})


class CreateView(CustomLoginRequiredMixin):

    template = 'form.html'

    def get_context_data(self, form):
        return {'form': form,
                'title': _('Create status'),
                'button_text': _('Create')
                }

    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, self.template, self.get_context_data(form))

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Status created successfully"))
            form.save()
            return redirect('/statuses/')
        return render(request, self.template, self.get_context_data(form))


class UpdateView(CustomLoginRequiredMixin):

    template = 'form.html'

    def get_context_data(self, form, status):
        return {'form': form,
                'status': status,
                'title': _('Update status'),
                'button_text': _('Update')
                }

    def get_status(self):
        status_id = self.kwargs.get('pk')
        return get_object_or_404(Status, pk=status_id)

    def get(self, request, *args, **kwargs):
        status = self.get_status()
        form = StatusForm(instance=status)
        return render(request, self.template, self.get_context_data(form, status))

    def post(self, request, *args, **kwargs):
        status = self.get_status()
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Status successfully changed"))
            form.save()
            return redirect('/statuses/')
        return render(request, self.template, self.get_context_data(form, status))


class DeleteView(CustomLoginRequiredMixin):

    def get_status(self):
        status_id = self.kwargs.get('pk')
        return get_object_or_404(Status, pk=status_id)

    def get_context_data(self, status):
        return {
            'status': status,
            'title': _('Delete status'),
            'text': _('Are you sure you want to delete'),
            'button_text': _('Yes, delete')
        }

    def get(self, request, *args, **kwargs):
        status = self.get_status()
        return render(request, 'statuses/delete.html', self.get_context_data(status))

    def post(self, request, *args, **kwargs):
        status = self.get_status()
        if status:
            if Task.objects.filter(status=status).exists():
                messages.error(request, _("Cannot delete status because it is in use."))
                return redirect('/statuses/')
            else:
                status.delete()
                messages.success(request, _("Status successfully deleted"))
        return redirect('/statuses/')
