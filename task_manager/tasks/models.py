from django.db import models
from django.contrib.auth.models import User

from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(User, related_name='author',  on_delete=models.PROTECT)
    worker = models.ForeignKey(User, related_name='worker', on_delete=models.PROTECT)
    inserted_timestamp = models.DateTimeField(auto_now_add=True)
