from django.db import models
from encoder.signals import file_encoded

class ZencoderJob(models.Model):
    zencoder_id = models.PositiveIntegerField()
    url = models.CharField(max_length=1000)
    file = models.CharField(max_length=1000)
    outputs = models.ManyToManyField('ZencoderJobOutput')
    status = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.CharField(max_length=100, null=True)

    def send_signal_encoded(self):
        outs = []
        for o in self.outputs.all():
            o.append((o.label, o.file))
        file_encoded.send(sender=self, source_file=file, outputs=outs, thumbnails=None)

class ZencoderJobOutput(models.Model):
    url = models.CharField(max_length=1000)
    label = models.CharField(max_length=100, null=True)
    file = models.CharField(max_length=1000)
    zencoder_id = models.PositiveIntegerField() 
    progress = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    current = models.CharField(max_length=20)
