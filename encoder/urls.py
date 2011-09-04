from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'encoder.views.home'),
    url(r'^encode/$', 'encoder.views.encode'),
    url(r'^jobs/$', 'encoder.views.jobs'),
    url(r'^job/(?P<job_id>[0-9]+)$', 'encoder.views.job'),
    url(r'^notify', 'encoder.views.notify'),
)
