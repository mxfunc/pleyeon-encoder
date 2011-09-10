from django.db import models
from encoder.signals import file_encoded

class ZencoderJobManager(models.Manager):
    def get_jobs_in_progress(self):
        return self.exclude(status__in=self.model.job_not_in_progress)

class ZencoderJob(models.Model):
    jobs_in_progress = ZencoderJobManager()

    zencoder_id = models.PositiveIntegerField()
    url = models.CharField(max_length=1000)
    file = models.CharField(max_length=1000)
    outputs = models.ManyToManyField('ZencoderJobOutput')
    status = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.CharField(max_length=100, null=True)
    
    job_in_progress = ["pending", "waiting", "processing"]
    job_not_in_progress = ["finished", "cancelled", "failed"]
    
    def update_via_zencoder(self, zen):
        if self.status.lower() in self.job_not_in_progress:
            return
        job_details = zen.job.details(self.zencoder_id)
        if job_details.code == 200:
            self.status = job_details.body["job"]["status"]
            self.save()
        for output in outputs.all():
            output.update_via_zencoder(zen)

    def done(self):
        return not self.status in self.job_not_in_progress

    def send_signal_encoded(self):
        outs = []
        for o in self.outputs.all():
            outs.append((o.label, o.file))
        file_encoded.send(sender=self, source_file=file, outputs=outs, thumbnails=None)

class ZencoderJobOutput(models.Model):
    url = models.CharField(max_length=1000)
    label = models.CharField(max_length=100, null=True)
    file = models.CharField(max_length=1000)
    zencoder_id = models.PositiveIntegerField() 
    progress = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    current = models.CharField(max_length=20)

    output_in_progress = ["waiting", "queued", "assigning", "processing"]
    output_not_in_progress = ["finished", "cancelled", "failed", "no input"]

    def update_via_zencoder(self, zen):
        if self.status.lower() in self.output_not_in_progress:
            return
        output_details = zen.output.progress(self.zencoder_id)
        if output_details.code == 200:
            self.status = output_details.body['state']
            try:
                self.current = output_details.body['current_event']
                self.progress = output_details.body['progress']
            except KeyError:
                pass
            self.save()

    def done(self):
        return self.status in self.output_not_in_progress

