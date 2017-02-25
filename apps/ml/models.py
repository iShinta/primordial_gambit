from __future__ import unicode_literals

from django.db import models

class ReviewManager(models.Manager):
	kw = {
			'fire' : ['fire', 'buring', 'burn'],
			'shooting': ['shots fired', 'shooting', 'gun fire'],
			'flood': ['water', 'flooding']
	}

def clean_data(data):
	data = 'there are 100 to 150 people here'
	p_index = data.find('people')
	print p_index
	if p_index:
		people = max([int(s) for s in data[max(0,p_index-20):p_index].split() if s.isdigit()][0])
	print people

def category(keywords):
	for word in keywords:
		for i in kw:
				if word in kw[i]:
						return i


# Create your models here.
class Incident(models.Model):
	priority = models.IntegerField()
	is_resolved = models.BooleanField(default=False)
	category = models.CharField(max_length= 30)
	location = models.CharField(max_length= 250)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Call(models.Model):
	raw_text = models.TextField()
	parsed_text = models.TextField()
	location = models.CharField(max_length= 250)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	incident_id = models.ForeignKey(Incident, related_name="calls")