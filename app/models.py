from django.db import models
from django.utils import timezone


class File(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    amt = models.CharField(max_length=50, null=True, blank=True)
    image = models.FileField(upload_to="media/image", null=True, blank=True)