from django.conf.urls import patterns, include, url
from views import save


urlpatterns = patterns('',
    url(r'^api/save/', save, name="live_edit_save")
)