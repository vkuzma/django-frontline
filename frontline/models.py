from django.db import models


class Entry(models.Model):
    data = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=250, unique=True)

    def __unicode__(self):
        return self.name


class ImageEntry(models.Model):
    data = models.ImageField(upload_to='frontline/images', blank=True, null=True)
    name = models.CharField(max_length=250, unique=True)

    def __unicode__(self):
        return self.name
