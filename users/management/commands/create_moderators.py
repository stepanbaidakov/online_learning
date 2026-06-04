from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create moderators'
    def handle(self, *args, **options):
        moderator, created = Group.objects.get_or_create(name='moderator')
        view_lesson_permission = Permission.objects.get(codename='view_lesson')
        view_course_permission = Permission.objects.get(codename='view_course')
        update_lesson_permission = Permission.objects.get(codename='change_lesson')
        update_course_permission = Permission.objects.get(codename='change_course')
        moderator.permissions.add(view_lesson_permission)
        moderator.permissions.add(view_course_permission)
        moderator.permissions.add(update_lesson_permission)
        moderator.permissions.add(update_course_permission)
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'moderator' успешно создана"))
        else:
            self.stdout.write(self.style.SUCCESS('Права группы "moderator" обновлены'))