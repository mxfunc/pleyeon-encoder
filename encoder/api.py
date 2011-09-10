from django.conf import settings
import os, shutil, stat

from encoder.utils import zencoder_add_job

def zencoder_submit_sync(file_path, thumbnails=True):
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        work_dir = settings.ZENCODER_WORK_DIR
        video_profiles = settings.ZENCODER_PROFILES
        thumbnail_profiles = settings.ZENCODER_THUMBNAIL_PROFILES if thumbnails else None
        notify_url = settings.ZENCODER_NOTIFY_URL
        upload_prefix = settings.ZENCODER_UPLOAD_PREFIX
        
        file_name = os.path.basename(file_path)
        if os.path.isdir(work_dir):
            shutil.copy(file_path, work_dir)
            os.chmod(os.path.join(work_dir, file_name), stat.S_IROTH)
        else:
            raise ValueError("ENCODER_WORK_DIR is not a directory")

        input_url_prefix = settings.ZENCODER_DOWNLOAD_PREFIX
        input_url = input_url_prefix + input_path if input_url_prefix.endswith('/') else input_url_prefix + '/' + file_name 
        zencoder_add_job(file_path, input_url, upload_prefix, notify_url, video_profiles, thumbnail_profiles)
    else:
        raise ValueError("file_path does not exist or is not a file")

def zencoder_submit(list_of_files):
    for file in list_of_files:
        zencoder_submit_sync(file)
