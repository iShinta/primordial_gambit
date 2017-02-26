from __future__ import unicode_literals
import requests
from django.db import models
from math import radians, cos, sin, asin, sqrt
import re
from django.core import serializers

class IncidentManager(models.Manager):

    def people_affected(self,raw_text):
		p_index = raw_text.find('people')
		people = 0
		if p_index:
			people = max([int(s) for s in raw_text[max(0,p_index-20):p_index].split() if s.isdigit()])
		return people

    def category(self,raw_text):
		kw = {
		'fire' : ['fire', 'buring', 'burn','smoke'],
		'shooting': ['shots fired', 'shooting', 'gun fire'],
		'flood': ['water', 'flooding'],
		'natural disaster': ['avalanche', 'earth quake'],
		}
		raw_text = raw_text.split()
		for word in raw_text:
			for k in kw:
				if word in kw[k]:
					print "*" * 50 , k
					return k
		return 'unknown'

    def location(self,raw_text):
		reg = re.compile(r"(?P<location>(.[0-9]+).{0,20}(lane|road|street))")
		m =  re.search(reg,raw_text.lower())
		try:
			m = m.groupdict()['location'].split()
			m.extend(['austin','texas'])
			m = "+".join([i for i in m])
			url = 'https://maps.googleapis.com/maps/api/geocode/json'
			params = {'sensor': 'false', 'address': m}
			result = requests.get(url, params=params).json()['results'][0]['geometry']['location']
			loc = [result['lng'],result['lat']]
		except:
			loc = ''
		return loc, m


    def create_incident(self,data,raw_text):
    	incidents = self.filter(is_resolved=False)
    	if len(incidents) != 0:
    		for incident in incidents:
    			location =  incident.location.replace("[","").replace("]","").split(',')
    			if location[0] != '':
                    loc = [data['location'][0],data['location'][1],float(location[0]),float(location[1])]
                    print loc
                    distance = self.haversine(loc)
                    print '----------------------' , distance
                    if distance <= 1.6  and incident.category == data['category']:
                    	return Call.objects.create(raw_text=raw_text,people=data['people_affected'],location=data['location'],incident=incident)
    	incident = self.create(priority = data['people_affected']+1,
																			category = data['category'],
																			location = data['location'],
																			people = data['people_affected'],
                                                                            address = data['address']
		)
		call = Call.objects.create(raw_text=raw_text,people=data['people_affected'],location=data['location'],incident=incident)
		return 'new incedent added'

    def parse_text(self,raw_text):
        location, address = self.location(raw_text)

        data = {
        	'people_affected': self.people_affected(raw_text),
        	'category': self.category(raw_text),
        	'location': location,
            'address': address
        }
        self.create_incident(data,raw_text)

    def haversine(self,loc):
		loc = [radians(float(i)) for i in loc]
		dlon = loc[2] - loc[0]
		dlat = loc[3] - loc[1]
		a = sin(dlat/2)**2 + cos(loc[1]) * cos(loc[3]) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a))
		km = 6367.0 * c
		return km


# Create your models here.
class Incident(models.Model):
    priority = models.IntegerField()
    people = models.IntegerField()
    is_resolved = models.BooleanField(default=False)
    category = models.CharField(max_length= 30)
    location = models.CharField(max_length= 250)
    address = models.CharField(max_length= 250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = IncidentManager()
class Call(models.Model):
	raw_text = models.TextField()
	# parsed_text = models.TextField()
	people = models.IntegerField()
	location = models.CharField(max_length= 250)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	incident = models.ForeignKey(Incident, related_name="calls")
	# objects = IncidentManager()
