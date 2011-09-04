# Create your views here.
import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from encoder.models import ZencoderJob, ZencoderJobOutput
from encoder.utils import listdir, zencoder_submit
from encoder.utils import zen

def encode(request):
    if request.method == 'GET':
        return render_to_response('encoder/encode.html', {'files':listdir()}, context_instance=RequestContext(request)) 
    else:
        files = request.REQUEST.getlist('files')
        zencoder_submit(files)
        return render_to_response('encoder/encode.html', {'files':listdir()}, context_instance=RequestContext(request))

def job(request, job_id):
    pass

def home(request):
    num_jobs = ZencoderJob.objects.all().count()
    num_jobs_finished = ZencoderJob.objects.filter(status__iexact='finished').count()
    num_jobs_failed = ZencoderJob.objects.filter(status__iexact='failed').count()
    num_jobs_processing = ZencoderJob.objects.filter(status__iexact='processing').count()
    num_jobs_pending = ZencoderJob.objects.filter(status__iexact='pending').count()
    num_jobs_waiting = ZencoderJob.objects.filter(status__iexact='waiting').count()

    num_outputs = ZencoderJobOutput.objects.all().count()

    num_outputs_finished = ZencoderJob.objects.filter(status__iexact='finished').count()
    num_outputs_failed = ZencoderJob.objects.filter(status__iexact='failed').count()
    num_outputs_processing = ZencoderJob.objects.filter(status__iexact='processing').count()
    num_outputs_pending = ZencoderJob.objects.filter(status__iexact='pending').count()
    num_outputs_waiting = ZencoderJob.objects.filter(status__iexact='waiting').count()


    num_outputs_inspecting = ZencoderJobOutput.objects.filter(current__iexact='Inspecting').count()
    num_outputs_downloading = ZencoderJobOutput.objects.filter(current__iexact='Downloading').count()
    num_outputs_transcoding = ZencoderJobOutput.objects.filter(current__iexact='Transcoding').count()
    num_outputs_uploading = ZencoderJobOutput.objects.filter(current__iexact='Uploading').count()
    return render_to_response('encoder/home.html', locals())

@csrf_exempt
def notify(request):
    if request.method != 'POST':
        return HttpResponseNotFound()
    if not request.raw_post_data:
        return HttpResponseNotFound()
    resp = json.loads(request.raw_post_data)
    try:
        job_id = resp['job']['id']
        o = ZencoderJob.objects.get(zencoder_id__exact=job_id)
        o.status = resp['job']['state']
        o.save()
        if 'output' in resp['job']:
            output_id = resp['job']['output']['id']
            output = o.outputs.filter(zencoder_id=output_id)
            output.state=resp['job']['output']['state']
            output.save()
    except:
        return HttpResponseServerError("I don't have that here, honey\n")
    ####### ADD CODE TO CREATE MODEL IF STATUS == FINISHED########
    
    return HttpResponse(job_id + " updated successfully", status=201)

def jobs(request):
    sort = request.REQUEST.get('sort', 'date') 
    order = request.REQUEST.get('order', None) 
    status = request.REQUEST.get('status', None)
    zencoder_get = request.REQUEST.get('zencoder', False)
    zencoder_get = True if zencoder_get=="true" else False
    
    try:
        page = int(request.REQUEST.get('page', 1))
    except:
        page = 1
    
    try:
        per_page = int(request.REQUEST.get('page', 10))
    except:
        per_page = 10

    qs = ZencoderJob.objects.all()
    if status:
        qs = qs.filter(status__exact=status)
    if sort == 'date': 
        if order =='asc':
            qs = qs.order_by('created_at')
        else:
            qs = qs.order_by('-created_at')
    elif sort == 'id':
        if order =='asc':
            qs = qs.order_by('id')
        else:
            qs = qs.order_by('-id')

    start = per_page*(page-1)
    end = per_page*page
    list_o = []
    for o in qs[start:end]:
        if zencoder_get:
            job_details = zen.job.details(o.zencoder_id)
            if job_details.code == 200:
                o.status = job_details.body["job"]["state"]
                o.save()
                for output in o.outputs.all():
                    output_details = zen.output.progress(output.zencoder_id)
                    if output_details.code == 200:
                        output.status = output_details.body['state']
                        try:
                            output.current = output_details.body['current_event']
                            output.progress = output_details.body['progress']
                        except KeyError:
                            pass
                        output.save()
        list_o.append(o)

    return render_to_response('encoder/jobs.html', {'jobs':list_o})