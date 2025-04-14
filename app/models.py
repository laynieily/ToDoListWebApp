from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('assigner', 'Assigner'),
        ('assignee', 'Assignee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='assignee')

class Task(models.Model):
    text = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)