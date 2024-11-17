import csv
import pytz
import random
import pandas as pd
from django.http import JsonResponse
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from .models import LifeBeingEvent, IaqEvent, Pointer
from django.db import transaction


def get_device_model():
    return LifeBeingEvent if settings.DEVICE_TYPE == 'lifebeing' else IaqEvent

@transaction.atomic
def load_data():
    print("Loading Data ...")
    model = get_device_model()
    csv_path = settings.LIFE_BEING_SENSOR_CSV_PATH if settings.DEVICE_TYPE == 'lifebeing' else settings.IAQ_SENSOR_CSV_PATH
    with open(csv_path, 'r') as csvfile:
        instances = []
        chunk_size = 1000  # Adjust the chunk size as necessary
        chunks = pd.read_csv(csvfile, chunksize=chunk_size, nrows=10000)
        sensor_data = pd.concat(chunks).to_dict(orient='records')
        for row in sensor_data:
            row['datetime'] = make_aware(datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S.%f'), timezone=pytz.UTC) # FIXME: specify container timezone???
            if settings.DEVICE_TYPE == 'lifebeing':
                row['value'] = row['value'].strip('\"')
            instances.append(model(**row))
        model.objects.bulk_create(instances, ignore_conflicts=True)
    print("Load Data Successfully!")

def random_timestamp():
    # Get the current time
    now = datetime.now()

    # Calculate the time 5 seconds ago
    five_seconds_ago = now - timedelta(seconds=5)

    # Generate a random number of seconds between 0 and 5
    random_ms = random.randint(0, 5000)

    # Create the random time by subtracting random seconds from now
    random_time = now - timedelta(milliseconds=random_ms)

    return random_time

# View for getting sensor data by device_id
@transaction.atomic
def get_sensor_data(request):
    # Keep pointer state in SQLite
    pointer = Pointer.objects.filter(device_id=settings.DEVICE_ID).first()
    offset = pointer.offset if pointer is not None else 0
    limit = random.randint(1, 5)

    data = pd.DataFrame(list(get_device_model().objects.all().values()[offset: offset+limit]))
    if len(data) > 0:
        data = data.drop(columns=['id'])
        data['datetime'] = data['datetime'].apply(lambda x: random_timestamp())
        data['device_id'] = settings.DEVICE_ID

    Pointer.objects.update_or_create(device_id=settings.DEVICE_ID, defaults={ 'offset': offset+limit if len(data) >= limit else 0 })

    return JsonResponse(data.to_dict(orient='records'), safe=False)
