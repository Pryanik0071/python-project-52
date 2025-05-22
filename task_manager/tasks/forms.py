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

        # Создаем список выбора с пустым элементом и полными именами
        users = User.objects.order_by('id')
        choices = [('', '---------')]  # Пустой выбор
        choices += [
            (user.id, f"{user.first_name} {user.last_name}") for user in users
        ]

        # Настраиваем виджет
        self.fields['executor'].widget = forms.Select(choices=choices)
