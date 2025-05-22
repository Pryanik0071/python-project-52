from django import forms
from django.contrib.auth.models import User

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'executor',
            'labels'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Отсортировать пользователей по id
        self.fields['executor'].queryset = User.objects.all().order_by('id')
