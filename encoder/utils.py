import os
import time
import datetime
import urllib
import shutil
from zencoder import Zencoder

from encoder.models import ZencoderJob, ZencoderJobOutput 
from encoder.settings import ZENCODER_OUTPUT_DIR, ZENCODER_WORK_DIR
from encoder.settings import ZENCODER_API_KEY, ZENCODER_NOTIFY_URL
from encoder.settings import DOWNLOAD_PREFIX, UPLOAD_PREFIX, FTP_DIR
from encoder.zencoder_profiles import *

zen = Zencoder(ZENCODER_API_KEY)
HOME_DIR = FTP_DIR

######## FILTER MEDIA FILES ########
MEDIA_FILES_SUFFIXES = [
'avi','dat','vob','mp4','mpg','mpeg','flv','f4v'
]
#### ZENCODER RESPONSE CODES ######
ZENCODER_JOB_OK = 201

#### A HACK #########
def is_being_written(f):
    return abs(time.mktime(datetime.datetime.now().timetuple())-os.stat(f).st_mtime) < 10

def listdir(d=HOME_DIR, abs_path=False, size=True):
    list_of_files = []
    for f in os.listdir(HOME_DIR):
        abs_f = os.path.join(HOME_DIR, f)
        if not os.path.isdir(f) and not is_being_written(abs_f):
            f = abs_f if abs_path else f
            size_m = float(os.path.getsize(abs_f))/1000000.0
            t = {'file':f, 'size':size_m} if size else f
            list_of_files.append(t)
    return list_of_files

def zencoder_create_job(input_url):
    input_url=DOWNLOAD_PREFIX+"singham.avi"
    print input_url
    smartphone = {'base_url':UPLOAD_PREFIX} 
    smartphone_advanced = {'base_url':UPLOAD_PREFIX}
    notifications = {"notifications":ZENCODER_NOTIFY_URL}
    
    smartphone.update(UNIVERSAL_SMARTPHONE)
    smartphone_advanced.update(ADVANCED_SMARTPHONE)
    smartphone.update(notifications)
    smartphone_advanced.update(notifications)
    outputs = (smartphone, smartphone_advanced)
    
    return zen.job.create(input_url, outputs=outputs)
 
def zencoder_submit(list_of_files):
    for file in list_of_files:
        abs_input_file_path = os.path.join(HOME_DIR, file)
        abs_output_file_path = os.path.join(ZENCODER_OUTPUT_DIR, file)
        job = zencoder_create_job(DOWNLOAD_PREFIX+urllib.quote(file))
        print job.body
        if job.code == ZENCODER_JOB_OK:
            if os.path.isdir(ZENCODER_WORK_DIR):
                dst_file = os.path.join(ZENCODER_WORK_DIR, file)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                moved = False
                shutil.move(abs_input_file_path, ZENCODER_WORK_DIR)
                moved = True
                try:
                    o = ZencoderJob.objects.create(zencoder_id=job.body['id'], file=abs_output_file_path)
                    for output in job.body['outputs']:
                        o.outputs.add(ZencoderJobOutput.objects.create(file=abs_input_file_path, zencoder_id=output['id'], url=output['url'], label=output['label']))
                except:
                    if moved:
                        shutil.move(dst_file, HOME_DIR)
                    raise