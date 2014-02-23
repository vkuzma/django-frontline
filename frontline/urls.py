from django.conf.urls import patterns, include, url
from views import save, richtext_form,  ImageUploadFormView, RichtextFormView


urlpatterns = patterns('',
    url(r'^api/save/', save, name='frontline_save'),
    url(r'^api/richtext-form/(?P<name>[\w\-]+)/$', RichtextFormView.as_view(), name='frontline_richtext_form'),
    url(r'^api/image-upload-form/(?P<name>[\w\-]+)/$', ImageUploadFormView.as_view(), name='frontline_image_upload')
)