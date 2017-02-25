from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Call(models.Model):
    raw_text = models.TextField()
    parsed_text = models.TextField()
    location = models.CharField(max_length= 250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    incident_id = models.ForeignKey(Incident, related_name="calls")




class Incident(models.Model):
    priority = models.IntegerField()
    is_resolved = models.BooleanField(initial=False)
    category = models.CharField(max_length= 30)
    location = models.CharField(max_length= 250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
