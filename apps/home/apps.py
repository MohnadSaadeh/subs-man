from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.home'  # Adjust this based on your project structure

    def ready(self):
        import apps.home.signals  #  Import signals when Django starts
