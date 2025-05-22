from django.db import models
from django.contrib.auth.models import User

from task_manager.statuses.models import Status
from task_manager.labels.models import Label

from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Name"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name=_("Status"))
    author = models.ForeignKey(User, related_name='authored_tasks',  on_delete=models.PROTECT,
                               verbose_name=_("Author"))
    executor = models.ForeignKey(
        User,
        related_name='executed_tasks',
        on_delete=models.PROTECT,
        verbose_name=_("Executor"),
        blank=True,
        null=True
    )
    labels = models.ManyToManyField(
        Label,
        related_name="tasks",
        verbose_name=_("Labels"),
        blank=True,
    )
    inserted_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
