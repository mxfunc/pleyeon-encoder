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
     
    def handle(self, *args, **options):
        if options["verbose"]:
            self.stdout.write("Job ID - \t Status \n\n")
        jobs = ZencoderJob.objects.get_jobs_in_progress()
        for j in jobs:
            j.update_via_zencoder(zen)
            if options["verbose"]:
                self.stdout.write(str(j.zencoder_id)+"\t"+j.status+"\n")
        """ 
        outputs = ZencoderJobOutput.objects.exclude(status__in=self.output_not_in_progress)
        if options["verbose"]:
            self.stdout.write("\nOutput ID - \t Status \n\n")
        for o in outputs:
            o.update_via_zencoder(zen)
            if options["verbose"]:
                self.stdout.write(str(o.zencoder_id)+"\t"+o.status+"\n")
        """
