from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('assigner', 'Assigner'),
        ('assignee', 'Assignee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='assignee')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Task(models.Model):
    text = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_assigned_to_me'
    )
    assigner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_I_created'
    )

    def __str__(self):
        return f"{self.text} - {'✔' if self.completed else '✘'}"
