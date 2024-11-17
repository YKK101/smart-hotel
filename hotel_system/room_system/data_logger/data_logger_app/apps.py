from django.apps import AppConfig
from django.conf import settings
from .services.mqtt_service import MQTTService
import os


class DataLoggerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_logger_app'

    mqtt_client = None

    def ready(self):
        # Skip initialization for child processes created by the auto-reloader
        if os.environ.get('RUN_MAIN', None) != 'true':
            return  # Avoid re-initialization in child processes

        import data_logger_app.signals
        # Start MQTT client when the app is ready
        broker = settings.MQTT_BROKER
        port = int(settings.MQTT_PORT)
        topic = settings.MQTT_TOPIC
        username = getattr(settings, 'MQTT_USERNAME', None)
        password = getattr(settings, 'MQTT_PASSWORD', None)

        self.mqtt_client = MQTTService(broker, port, topic, username, password)
        self.mqtt_client.start()

    def shutdown(self):
        # Cleanly shut down MQTT client on app termination
        if self.mqtt_client:
            self.mqtt_client.stop()