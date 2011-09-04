from django.db import models
from encoder.settings import FTP_DIR, ZENCODER_OUTPUT_DIR

class ZencoderJob(models.Model):
    zencoder_id = models.PositiveIntegerField()
    url = models.CharField(max_length=1000)
    file = models.CharField(max_length=1000)
    outputs = models.ManyToManyField('ZencoderJobOutput')
    status = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.CharField(max_length=100, null=True)

class ZencoderJobOutput(models.Model):
    url = models.CharField(max_length=1000)
    label = models.CharField(max_length=100, null=True)
    file = models.CharField(max_length=1000)
    zencoder_id = models.PositiveIntegerField() 
    progress = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    current = models.CharField(max_length=20)
