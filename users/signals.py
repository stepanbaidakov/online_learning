from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django_celery_beat.models import IntervalSchedule, PeriodicTask


@receiver(post_migrate)
def create_periodic_task(**kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.DAYS,
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Block inactive users",
        task="users.tasks.block_inactive_users",
    )
