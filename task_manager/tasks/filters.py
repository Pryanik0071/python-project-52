import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import Task, Label


class UserFullNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class UserFullNameModelChoiceFilter(django_filters.ModelChoiceFilter):
      field_class = UserFullNameChoiceField


class TaskFilter(django_filters.FilterSet):
    executor = UserFullNameModelChoiceFilter(
        queryset=User.objects.all().order_by('id'),
        label=_("Executor")
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label')
    )

    own_tasks = django_filters.BooleanFilter(
        label=_('Only own tasks'),
        widget=forms.CheckboxInput,
        method='get_self_tasks',
    )

    def get_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status']
