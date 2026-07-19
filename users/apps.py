from importlib import import_module

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import_module("users.signals")
