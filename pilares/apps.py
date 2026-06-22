from django.apps import AppConfig


class PilaresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pilares'
    
    def ready(self):
        import pilares.signals  # ← Agrega esta línea
