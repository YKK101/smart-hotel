# signals.py
from django.dispatch import receiver
from .services.mqtt_service import mqtt_message_received
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from .views import handle_occupancy_update
import json


# Receiver function that is triggered when an MQTT message is received
@receiver(mqtt_message_received)
def handle_mqtt_message(sender, topic, message, **kwargs):
    """Process the MQTT message and call a view function or custom logic."""
    handle_occupancy_update(topic, json.loads(message))
