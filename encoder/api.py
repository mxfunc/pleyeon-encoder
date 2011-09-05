from django.conf import settings
import os, shutil

from encoder.utils import zencoder_add_job

def zencoder_submit_sync(file_path, thumbnails=True):
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        work_dir = settings.ENCODER_WORK_DIR
        video_profiles = settings.ZENCODER_PROFILES
        thumbnail_profiles = settings.ZENCODER_THUMBNAIL_PROFILES if thumbnails else None
        notify_url = settings.ZENCODER_NOTIFY_URL
        upload_prefix = setting.ZENCODER_UPLOAD_PREFIX
        
        if os.path.isdir(work_dir):
            shutil.copy(file_path, work_dir)
        else:
            raise ValueError("ENCODER_WORK_DIR is not a directory")

        input_url_prefix =  settings.ZENCODER_DOWNLOAD_PATH
        input_path = os.path.join(work_dir, os.path.basename(file_path))
        input_url = input_url_prefix[:-1] + input_path if input_url_prefix.endswith('/') else input_url_prefix + input_path 
        job = zencoder_add_job(file_path, input_url, upload_prefix, notify_url, video_profiles, thumbnail_profiles)
    else:
        raise ValueError("file_path does not exist or is not a file")

def zencoder_submit(list_of_files):
    for file in list_of_files:
        zencoder_submit_sync(file)
