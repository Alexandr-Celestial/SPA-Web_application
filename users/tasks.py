from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivated_users():
    time_zone = timezone.now() - timedelta(days=30)
    users_to_deactivate = User.objects.filter(last_login__lt=time_zone, is_active=True)
    users_to_deactivate.update(is_active=False)