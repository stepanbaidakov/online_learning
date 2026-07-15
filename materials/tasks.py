from django.core.mail import send_mail

from celery import shared_task

from config.settings import DEFAULT_FROM_EMAIL

from .models import Subscription


@shared_task
def send_course_mail(course_id):
    subscriptions = Subscription.objects.filter(course_id=course_id)
    for subscription in subscriptions:
        try:
            send_mail(
                subject="Обновление курса из подписки",
                message="Курс, на который в оформили подписку, обновился. Зайдите и проверьте что есть нового.",
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.user.email],
            )
        except Exception as e:
            print(e)
