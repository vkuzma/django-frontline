from django.db import models


class Entry(models.Model):
    data = models.TextField(blank=True, null=True)
    anchor = models.CharField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return self.anchor
