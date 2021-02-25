from django.apps import AppConfig


class InspectionConfig(AppConfig):
    name = 'inspection'
    def ready(self):
        import inspection.signals
