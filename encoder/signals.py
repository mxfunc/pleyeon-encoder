import django.dispatch

file_encoded = django.dispatch.Signal(providing_args=["source_file", "outputs", "thumbnails"]
