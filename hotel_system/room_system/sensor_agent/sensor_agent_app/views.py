from django.http import JsonResponse
from django.conf import settings
from django.apps import apps
from sensor_agent_app.utils import get_http_data
import time


def publish_message(message):
    mqtt_client = apps.get_app_config('sensor_agent_app').mqtt_client

    topic = settings.MQTT_TOPIC
    if settings.DEVICE_TYPE == 'lifebeing':
        datapoint = message.pop('datapoint')
        topic = f'{topic}/{datapoint}'

    if mqtt_client:
        mqtt_client.publish(topic, message)

# FIXME: Implement cronjobs outside this service or implement celery, just over-engineer for MVP purpose
def schedule_fetch_data():
    while True:
        transfer_data()
        time.sleep(5)

def transfer_data():
    data = get_http_data(settings.GET_SENSOR_DATA_URL)

    for record in data:
        publish_message(record)
    return JsonResponse({ 'success': True })
