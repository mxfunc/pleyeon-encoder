from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from encoder.models import ZencoderJob, ZencoderJobOutput
from encoder.utils import zen

class Command(BaseCommand):
    help = "update job status of unfinished jobs from zencoder"
    
    option_list = BaseCommand.option_list + (
        make_option("-w",
            action="store_true",
            dest="verbose",
            default=False,
            help="print job ids updated"),
        )
     
    job_in_progress = ["pending", "waiting", "processing"]
    output_in_progress = ["waiting", "queued", "assigning", "processing"]

    job_not_in_progress = ["finished", "cancelled", "failed"]
    output_not_in_progress = ["finished", "cancelled", "failed", "no input"]
    #job_not_in_progress = ["processing"]

    def handle(self, *args, **options):
        if options["verbose"]:
            self.stdout.write("Job ID - \t Status \n\n")
        jobs = ZencoderJob.objects.exclude(status__in=self.job_not_in_progress)
        for j in jobs:
            job_details = zen.job.details(j.id)
            if options["verbose"]:
                os.self.write(str(j.zencoder_id)+"\t"+j.status+"\n")
            if job_details.code == 200:
                j.status = job_details.body["job"]["state"]
                j.save()

        outputs = ZencoderOutputJobx.objects.exclude(status__in=self.output_not_in_progress)
        for o in j.outputs:
            self.stdout.write("\nOutput ID - \t Status \n\n")
            output_details = zen.output.progress(o.zencoder_id)
            if output_details.code == 200:
                o.status = output_details.body['state']
                try:
                    o.current = output_details.body['current_event']
                    o.progress = output_details.body['progress']
                except KeyError:
                    pass
                o.save()
            if options["verbose"]:
                os.self.write(str(o.zencoder_id)+"\t"+o.status+"\n")

