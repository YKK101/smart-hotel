from django.db import models
import uuid


class PresenceState(models.Model):
    device_id = models.TextField(primary_key=True)
    presence_state = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'presence_state'