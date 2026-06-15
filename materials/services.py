from django.utils import timezone
from .tasks import send_course_mail
from datetime import timedelta


def notify_if_needed(course):
    now = timezone.now()

    if now - course.updated_at > timedelta(hours=4):
        send_course_mail.delay(course.id)

    course.save()