from django.core.management.base import BaseCommand, CommandError
from materials.models import Course, Lesson
from users.models import Payment
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'create payments'

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            raise CommandError("Пользователь с id=1 не найден")
        try:
            course = Course.objects.get(id=1)
        except Course.DoesNotExist:
            raise CommandError("Курс с id=1 не найден")
        try:
            lesson = Lesson.objects.get(id=1)
        except Lesson.DoesNotExist:
            raise CommandError("Урок с id=1 не найден")
        amount1 = 1000
        amount2 = 500
        method1 = "Перевод на счет"
        method2 = "Наличные"
        created_payment1, created1 = Payment.objects.get_or_create(user=user, course=course, amount=amount1, method=method1)
        created_payment2, created2 = Payment.objects.get_or_create(user=user, lesson=lesson, amount=amount2, method=method2)
        if created1:
            self.stdout.write(self.style.SUCCESS("Платеж за курс успешно создан"))
        else:
            self.stdout.write(self.style.SUCCESS('Платеж за курс уже был создан'))

        if created2:
            self.stdout.write(self.style.SUCCESS("Платеж за урок успешно создан"))
        else:
            self.stdout.write(self.style.SUCCESS('Платеж за урок уже был создан'))
