from django.db import models


class LifeBeingEvent(models.Model):
    device_id = models.TextField()
    datapoint = models.TextField()
    value = models.TextField()
    datetime = models.DateTimeField()

    class Meta:
        db_table = 'lifebeing'
        constraints = [
            models.UniqueConstraint(fields=['device_id', 'datapoint', 'datetime'], name='unique_device_datapoint_datetime')
        ]

class IaqEvent(models.Model):
    device_id = models.TextField()
    noise = models.DecimalField(max_digits=10, decimal_places=2)
    co2 = models.DecimalField(max_digits=10, decimal_places=2)
    pm25 = models.DecimalField(max_digits=10, decimal_places=2)
    humidity = models.DecimalField(max_digits=10, decimal_places=2)
    temperature = models.DecimalField(max_digits=10, decimal_places=2)
    illuminance = models.DecimalField(max_digits=10, decimal_places=2)
    online_status = models.TextField()
    device_status = models.TextField()
    datetime = models.DateTimeField()

    class Meta:
        db_table = 'iaq'
        constraints = [
            models.UniqueConstraint(fields=['device_id', 'datetime'], name='unique_device_datetime')
        ]

class Pointer(models.Model):
    device_id = models.TextField(primary_key=True)
    offset = models.IntegerField(default=0)

    class Meta:
        db_table = 'pointer'