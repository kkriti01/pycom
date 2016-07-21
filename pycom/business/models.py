from __future__ import unicode_literals

from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=300)
    page_id = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    email = models.EmailField(max_length=200, blank=True)
    phone = models.CharField(max_length=300, blank=True)
    street = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    pin = models.CharField(max_length=10, blank=True)
    category = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-likes']
