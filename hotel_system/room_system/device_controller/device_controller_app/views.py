from django.shortcuts import render
import json
from .utils import put_http_data
import requests


def get_device_control_url(device_id):
    # Read the device configuration from the mounted JSON file
    with open('/app/configs/device-config.json') as f:
        device_mapping = json.load(f)

    return device_mapping.get(device_id)
    
def control_device(topic, message):
    payload = message['payload']
    control_url = get_device_control_url(message['device_id'])
    put_http_data(control_url, payload)
