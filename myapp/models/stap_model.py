from django.db import models
from .time_stamp import TimeStampedModel


class StapModel(TimeStampedModel):
    name = models.CharField(max_length=255)
    odoo_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
