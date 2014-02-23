from django.db import models


class Gallery(models.Model):
    name = models.CharField(max_length=250, unique=True)


class Image(models.Model):
    image = models.ImageField(upload_to='frontline/galleryimage')
    gallery = models.ForeignKey(Gallery, related_name='images')