from celery import shared_task
from django.contrib.auth import get_user_model
from rest_framework.utils import timezone
from datetime import timedelta

@shared_task
def check_inactive_users():
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)

    users = User.objects.filter(
        is_active=True,
        last_login__lt=month_ago
    )

    users.update(is_active=False)


@shared_task
def check_inactive_users():
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)

    users = User.objects.filter(is_active=True, last_login__lt=month_ago)

    for user in users:
        block_user.delay(user.id)