from django.apps import AppConfig


class DStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'd_store'
    
    def ready(self):
        import d_store.signals
