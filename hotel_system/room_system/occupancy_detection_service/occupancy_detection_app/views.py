from django.shortcuts import render
from django.conf import settings
from django.apps import apps
from django.db import transaction
import json
from .models import PresenceState


def get_control_device_id(sensor_device_id):
    # Read the device configuration from the mounted JSON file
    with open('/app/configs/sensor-to-device.json') as f:
        device_mapping = json.load(f)

    return device_mapping.get(sensor_device_id)

def publish_message(message):
    mqtt_client = apps.get_app_config('occupancy_detection_app').mqtt_client

    topic = settings.MQTT_PUBLISH_TOPIC
    if mqtt_client:
        mqtt_client.publish(topic, message)

# Create your views here.
@transaction.atomic
def handle_occupancy_update(topic, message):
    caches = PresenceState.objects.filter(device_id=message['device_id'])
    current = None
    if caches.exists():
        current = caches.first()

    publish_required = message['value'] == 'unoccupied' and (current is None or current.presence_state == 'occupied')
    print(f"Occupancy updated for {message['device_id']}, Energy saving adjust = {publish_required}")
    PresenceState.objects.update_or_create(device_id=message['device_id'], defaults={ 'device_id': message['device_id'], 'presence_state': message['value'] })


    if publish_required:
        publish_message({
            'device_id': get_control_device_id(message['device_id']),
            'payload': { 'temparature': 27 },
        })