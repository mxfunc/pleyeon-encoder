import os
import time
import datetime
import urllib
import shutil
from zencoder import Zencoder

from encoder.models import ZencoderJob, ZencoderJobOutput 
from encoder.settings import ZENCODER_WORK_DIR
from encoder.settings import ZENCODER_API_KEY, ZENCODER_NOTIFY_URL
from encoder.settings import ZENCODER_DOWNLOAD_PREFIX, ZENCODER_UPLOAD_PREFIX, FTP_DIR
from encoder.zencoder_profiles import *

zen = Zencoder(ZENCODER_API_KEY)
HOME_DIR = FTP_DIR

######## FILTER MEDIA FILES ########
MEDIA_FILES_SUFFIXES = [
'avi','dat','vob','mp4','mpg','mpeg','flv','f4v'
]
#### ZENCODER RESPONSE CODES ######
ZENCODER_JOB_OK = 201

def now_uts():
    return time.mktime(datetime.datetime.now())

#### A HACK #########
def is_being_written(f):
    return abs(time.mktime(now_uts())-os.stat(f).st_mtime) < 10

def listdir(d=HOME_DIR, size=True):
    list_of_files = []
    for f in os.listdir(HOME_DIR):
        abs_f = os.path.join(HOME_DIR, f)
        if not os.path.isdir(f) and not is_being_written(abs_f):
            size_m = float(os.path.getsize(abs_f))/1000000.0
            t = {'file':f, 'size':size_m} if size else f
	    t.update({'abs_path':abs_f})
            list_of_files.append(t)
    return list_of_files

def get_unique_output_name():
    import random
    while True:
        key = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(32))
        try:
            o = ZencoderOutput.objects.get(file=key)
        except ZencoderOutput.DoesNotExist:
            return key
        else:
            continue

def sha256_digest(s):
    import hashlib
    sha256 = hashlib.sha256()
    sha256.update(s)
    return sha256.hexdigest()

class JobNotCreatedException(Exception):
    pass

def zencoder_add_job(file_path, input_url, upload_prefix, notify_url=None, video_profiles=None, thumbnail_profiles=None):
    print input_url
    if notify_url:
        notifications = {"notifications":notify_url}
    base_url = {'base_url':upload_prefix}
    file_prefix = sha256_digest(file_path)[:32]+'_'+now_uts() 

    outputs = []
    for profile in video_profiles:
        filename = {'filename':file_prefix+'_'+profile['label']} 
        profile.update(filename)
        profile.update(notifications)
        profile.update(base_url)
        outputs.append(profile)

    for profile in thumbnail_profiles:
	#profile.update({label:"thumbails"})
        profile.update(base_url)
        outputs[0].update({'thumbnails':profile})

    job = zen.job.create(input_url, outputs=outputs)
    print job.body
    if job.code == ZENCODER_JOB_OK:
        zencoder_update_table(job, file_path)
    else:
        raise JobNotCreatedException("Zencoder job not created: response="+ str(job.body))

def zencoder_update_table(job, source_file_path):
    o = ZencoderJob.objects.create(zencoder_id=job.body['id'], file=source_file_path)
    for output in job.body['outputs']:
        filename = output['url'].split('/',1)[1]
        o.outputs.add(ZencoderJobOutput.objects.create(file=filename, zencoder_id=output['id'], url=output['url'], label=output['label']))
    o.save()


