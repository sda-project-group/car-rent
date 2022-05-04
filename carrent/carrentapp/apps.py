from django.apps import AppConfig


class CarrentappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carrentapp'

    def ready(self):
        import carrentapp.signals