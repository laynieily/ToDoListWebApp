from django import template
from ..models import TaskStatus

register = template.Library()

@register.filter
def get_user_status(statuses, user):
    return statuses.filter(user=user).first()
