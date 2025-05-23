from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import Label
from .forms import LabelForm
from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.tasks.models import Task


LABELS = '/labels/'


class IndexView(CustomLoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(request, 'labels/index.html', {'labels': labels})


class CreateView(CustomLoginRequiredMixin):

    template = 'form.html'

    def get_context_data(self, form):
        return {'form': form,
                'title': _('Create label'),
                'button_text': _('Create')
                }

    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request, self.template, self.get_context_data(form))

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Label created successfully"))
            form.save()
            return redirect(LABELS)
        return render(request, self.template, self.get_context_data(form))


class UpdateView(CustomLoginRequiredMixin):

    template = 'form.html'

    def get_context_data(self, form, label):
        return {'form': form,
                'label': label,
                'title': _('Update label'),
                'button_text': _('Update')
                }

    def get_label(self):
        label_id = self.kwargs.get('pk')
        return get_object_or_404(Label, pk=label_id)

    def get(self, request, *args, **kwargs):
        label = self.get_label()
        form = LabelForm(instance=label)
        return render(
            request, self.template, self.get_context_data(form, label)
        )

    def post(self, request, *args, **kwargs):
        label = self.get_label()
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _("Label successfully changed"))
            form.save()
            return redirect(LABELS)
        return render(
            request, self.template, self.get_context_data(form, label)
        )


class DeleteView(CustomLoginRequiredMixin):

    def get_label(self):
        label_id = self.kwargs.get('pk')
        return get_object_or_404(Label, pk=label_id)

    def get_context_data(self, label):
        return {
            'label': label,
            'title': _('Delete label'),
            'text': _('Are you sure you want to delete'),
            'button_text': _('Yes, delete')
        }

    def get(self, request, *args, **kwargs):
        label = self.get_label()
        return render(
            request, 'labels/delete.html', self.get_context_data(label)
        )

    def post(self, request, *args, **kwargs):
        label = self.get_label()
        if label:
            if Task.objects.filter(labels=label).exists():
                messages.error(
                    request,
                    _("Cannot delete label because it is in use.")
                )
                return redirect(LABELS)
            else:
                label.delete()
                messages.success(request, _("Label successfully deleted"))
        return redirect(LABELS)
