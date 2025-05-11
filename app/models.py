from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = [('assigner', 'Assigner'), ('assignee', 'Assignee')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    alarm_days = models.IntegerField()
    status = models.CharField(max_length=20, default='Not started')
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_tasks')
    assigner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        null=True,
        blank=True,
        related_name = 'tasks_created'
    )

    STATUS_CHOICES = [
    ('Not started', 'Not started'),
    ('In progress', 'In progress'),
    ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not started')

def __str__(self):
    return self.title


class TaskStatus(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='statuses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('Not started', 'Not started'),
        ('In progress', 'In progress'),
        ('Completed', 'Completed'),
    ], default='Not started')

    class Meta:
        unique_together = ('task', 'user')