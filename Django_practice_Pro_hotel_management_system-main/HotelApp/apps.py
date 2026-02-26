from django.apps import AppConfig


class HotelappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HotelApp'

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yourapp'

    def ready(self):
        import yourapp.signals
