"""App module"""
from django.apps import AppConfig


class MapsConfig(AppConfig):
    """AppConfig class"""
    name = 'core'
    #
    # def ready(self):
    #     from detection import update
    #     update.notify_user()
