from django.contrib import admin
from django.conf.urls import patterns, url
from .models import Entry, ImageEntry
from views import save, ImageUploadFormView, RichtextFormView


class EntryAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(EntryAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^save/', save, name='frontline_save'),
            url(r'^richtext-form/(?P<name>[\w\-]+)/$', RichtextFormView.as_view(), name='frontline_richtext_form'),
                           )
        return my_urls + urls


class ImageEntryAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(ImageEntryAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^image-upload-form/(?P<name>[\w\-]+)/$', ImageUploadFormView.as_view(), name='frontline_image_upload')
                           )
        return my_urls + urls



admin.site.register(Entry, EntryAdmin)
admin.site.register(ImageEntry, ImageEntryAdmin)


