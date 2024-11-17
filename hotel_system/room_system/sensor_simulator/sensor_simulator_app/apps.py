import os
from django.apps import AppConfig


class SensorSimulatorAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sensor_simulator_app'

    def ready(self):
        # Skip initialization for child processes created by the auto-reloader
        if os.environ.get('RUN_MAIN', None) != 'true':
            return  # Avoid re-initialization in child processes
        
        from .views import load_data
        load_data()