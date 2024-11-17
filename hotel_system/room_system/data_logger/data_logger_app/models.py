import uuid
from django.db import models
from django.utils.timezone import make_aware

class BaseLifeBeingEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField()
    hotel = models.TextField()
    floor = models.TextField()
    room = models.TextField()
    device_id = models.TextField()

    class Meta:
        abstract = True  # This class will not be used to create any table, only to be inherited
        indexes = [
            models.Index(fields=['datetime']),
            models.Index(fields=['hotel']),
            models.Index(fields=['floor']),
        ]

class LifeBeingOnlineStatusEvent(BaseLifeBeingEvent):
    value = models.TextField()

    class Meta:
        db_table = 'life_being_online_status_event'

class LifeBeingSensitivityEvent(BaseLifeBeingEvent):
    value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'life_being_sensitivity_event'

class LifeBeingPresenceStateEvent(BaseLifeBeingEvent):
    value = models.TextField()

    class Meta:
        db_table = 'life_being_presence_state_event'

class LifeBeingSensor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_updated = models.DateTimeField(auto_now=True)
    hotel = models.TextField()
    floor = models.TextField()
    room = models.TextField()
    device_id = models.TextField()
    online_status = models.TextField()
    sensitivity = models.TextField()
    presence_state = models.TextField()

    class Meta:
        db_table = 'life_being_sensor'
        indexes = [
            models.Index(fields=['hotel']),
            models.Index(fields=['floor']),
        ]

class BaseIaqSensor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.TextField()
    floor = models.TextField()
    room = models.TextField()
    device_id = models.TextField()
    noise = models.DecimalField(max_digits=10, decimal_places=2)
    co2 = models.DecimalField(max_digits=10, decimal_places=2)
    pm25 = models.DecimalField(max_digits=10, decimal_places=2)
    humidity = models.DecimalField(max_digits=10, decimal_places=2)
    temperature = models.DecimalField(max_digits=10, decimal_places=2)
    illuminance = models.DecimalField(max_digits=10, decimal_places=2)
    online_status = models.TextField()
    device_status = models.TextField()

    class Meta:
        abstract = True  # This class will not be used to create any table, only to be inherited

class IaqEvent(BaseIaqSensor):
    datetime = models.DateTimeField()

    class Meta:
        db_table = 'iaq_event'
        indexes = [
            models.Index(fields=['datetime']),
            models.Index(fields=['hotel']),
            models.Index(fields=['floor']),
        ]

class IaqSensor(BaseIaqSensor):
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'iaq_sensor'
        indexes = [
            models.Index(fields=['hotel']),
            models.Index(fields=['floor']),
        ]
