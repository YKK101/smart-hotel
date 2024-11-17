from django.shortcuts import render
from .models import LifeBeingOnlineStatusEvent, LifeBeingPresenceStateEvent, LifeBeingSensitivityEvent, LifeBeingSensor, IaqEvent, IaqSensor
import re
import json
from django.utils.timezone import make_aware
import pytz
from datetime import datetime
from decimal import Decimal
from django.db import transaction
import copy


def extract_topic_info(topic): # FIXME: Move to utils
    # Define the regex pattern
    pattern = r'^(?P<type>\w+)/hotels/(?P<hotel>\w+)/floors/(?P<floor>\w+)/rooms/(?P<room>\w+)(?:/(?P<datapoint>\w+))?$'

    # Match the topic string against the regex
    match = re.match(pattern, topic)

    if match:
        # If the pattern matches, return the captured groups
        return match.groupdict()
    else:
        # If the pattern doesn't match, return None
        return None

@transaction.atomic
def log_message_to_database(topic, message):
    info = extract_topic_info(topic)
    DATAPOINT_MODELS = {
        'online_status': LifeBeingOnlineStatusEvent,
        'presence_state': LifeBeingPresenceStateEvent,
        'sensitivity': LifeBeingSensitivityEvent,
    }

    if info['type'] == 'lifebeingsensor':
        event_model = DATAPOINT_MODELS.get(info['datapoint'])
        if event_model:
            value = Decimal(message['value']) if event_model == LifeBeingSensitivityEvent else message['value']
            default = {
                'hotel'       : info['hotel'],
                'floor'       : info['floor'],
                'room'        : info['room'],
                'device_id'   : message['device_id'],
            }
            event_data = {**default}
            event_data['datetime'] = make_aware(datetime.strptime(message['datetime'], '%Y-%m-%dT%H:%M:%S.%f'), timezone=pytz.UTC) # FIXME: specify container timezone???
            event_data['value'] = value
            event = event_model.objects.create(**event_data)
            event.save()

            update_data = {}
            update_data[info['datapoint']] = value
            sensor = LifeBeingSensor.objects.update_or_create(**default, defaults=update_data)
    
    elif info['type'] == 'iaqsensor':
        default = {
            'hotel'           : info['hotel'],
            'floor'           : info['floor'],
            'room'            : info['room'],
            'device_id'       : message['device_id'],
        }
        update_data = {
            'noise'           : Decimal(message['noise']),
            'co2'             : Decimal(message['co2']),
            'pm25'            : Decimal(message['pm25']),
            'humidity'        : Decimal(message['humidity']),
            'temperature'     : Decimal(message['temperature']),
            'illuminance'     : Decimal(message['illuminance']),
            'online_status'   : message['online_status'],
            'device_status'   : message['device_status'],
        }
        event_data = {**default, **update_data}
        event_data['datetime'] = make_aware(datetime.strptime(message['datetime'], '%Y-%m-%dT%H:%M:%S.%f'), timezone=pytz.UTC) # FIXME: specify container timezone???
            
        event = IaqEvent.objects.create(**event_data)
        event.save()

        sensor = IaqSensor.objects.update_or_create(**default, defaults=update_data)