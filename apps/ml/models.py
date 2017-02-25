from __future__ import unicode_literals
import requests
import simplejson
from django.db import models
from math import radians, cos, sin, asin, sqrt

class IncidentManager(models.Manager):
	kw = {
		'fire' : ['fire', 'buring', 'burn','smoke'],
		'shooting': ['shots fired', 'shooting', 'gun fire'],
		'flood': ['water', 'flooding']
	}

	def people_affected(raw_text):
		raw_text = 'there are 100 to 150 people here'
		p_index = raw_text.find('people')
		people = 0
		if p_index:
			people = max([int(s) for s in raw_text[max(0,p_index-20):p_index].split() if s.isdigit()][0])
		return people

	def category(raw_text):
		for word in raw_text:
			for category in kw:
					if word in kw[category]:
							return category
		return 'unknown'

	def location(raw_text):
		reg = re.compile(r"(?P<location>(.[0-9]+).{0,20}(lane|road|street))")
		m =  re.search(reg,raw_text.lower())
		m = m.groupdict()['location'].split()
		m.extend(['austin','texas'])
		m = "+".join([i for i in m])
		url = 'https://maps.googleapis.com/maps/api/geocode/json'
		params = {'sensor': 'false', 'address': m}
		result = requests.get(url, params=params).json()['results'][0]['geometry']['location']
		loc = [result['lng'],result['lat']]
		return loc

	def parse_text(raw_text):
		data = {
			'people_affected': self.people_affected(raw_text),
			'category': self.category(raw_text),
			'location': self.location(raw_text)
		}
		check_incident(data,raw_text)
	
	def haversine(lon1, lat1, lon2, lat2):
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
		dlon = lon2 - lon1 
		dlat = lat2 - lat1 
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a)) 
		km = 6367 * c
		return km

	def check_incident(data,raw_text):
		try:
			incidents = Incident.objects.filter(is_resolved=False)
		except:
			indicent = Incident.objects.create(priority = data['people_affected']+1,
																					category = data['category'],
																					location = data['location'],
																					people = data['people_affected']
			)
			call = Call.objects.create(raw_text=raw_text,people=data['people_affected'],location=data['location'],indicent=incident)
			return 'new incedent added'
		
		for incident in indicents:
			distance = haversine(data['location'][0],data['location'][1],incident['location'][0],indicent['location'][1])
			if distance <= 1.6  and call['category'] == data['category']:
				call = Call.objects.create(raw_text=raw_text,people=data['people_affected'],location=data['location'],indicent=incident)
			else:
				indicent = Incident.objects.create(priority = data['people_affected']+1,
																					category = data['category'],
																					location = data['location'],
																					people = data['people_affected']
			)
			call = Call.objects.create(raw_text=raw_text,people=data['people_affected'],location=data['location'],indicent=incident)
			return 'new incedent added'

# Create your models here.
class Incident(models.Model):
	priority = models.IntegerField()
	people = models.IntegerField()
	is_resolved = models.BooleanField(default=False)
	category = models.CharField(max_length= 30)
	location = models.CharField(max_length= 250)
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
