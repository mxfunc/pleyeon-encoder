## DEFAULT SETTINGS ##
"""
FTP_DIR=''
ZENCODER_WORK_DIR=''
ZENCODER_DOWNLOAD_PREFIX=''
ZENCODER_UPLOAD_PREFIX=''

ZENCODER_API_KEY=''
ZENCODER_NOTIFY_URL=''
"""

ZENCODER_PROFILES = (
    {
        "label":"universal_smartphone",
        "audio_bitrate" : 48,
        "audio_sample_rate" : 44100,
        "video_bitrate" : 250,
        "max_frame_rate" : 30,
        "size" : "480x320"
    },
    {
        "label":"advanced_smartphone",
        "h264_level": 3.1,
        "h264_profile": "main",
        "video_bitrate": 250,
        "max_video_bitrate": 400,
        "max_frame_rate": 30,
        "audio_bitrate": 48,
        "audio_sample_rate" : 44100,
        "size": "1280x720"
    },
)

ZENCODER_THUMBNAIL_PROFILES = (
    {
        "label":"png_150x80",
        "format":"png",
        "size":"150x80",
        "times":[4, 10],
        "filename":"{{number}}_{{size}}_thumbnail"
    },
)

ENCODER_DIR = (
)
try:
    from setting_local import *
except:
    pass

