from __future__ import unicode_literals

from django.db import models

class IncidentManager(models.Manager):
	kw = {
			'fire' : ['fire', 'buring', 'burn'],
			'shooting': ['shots fired', 'shooting', 'gun fire'],
			'flood': ['water', 'flooding']
	}

    def people_affected(raw_text):
    	raw_text = 'there are 100 to 150 people here'
    	p_index = raw_text.find('people')
    	print p_index
    	if p_index:
    		people = max([int(s) for s in raw_text[max(0,p_index-20):p_index].split() if s.isdigit()][0])
    	# print people
        return people

    def category(raw_text):
    	for word in raw_text:
    		for category in kw:
    				if word in kw[category]:
    						return category

    def location(raw_text):
        reg = re.compile(r"(?P<location>(.[0-9]+).{0,20}(lane|road|street))")
        m =  re.search(reg,string)
        print m.groupdict()['location']

    def parse_text(raw_text):
        people_affected = self.people_affected(raw_text)
        category = self.category(raw_text)
        location = self.location(raw_text)
        # do stuff not sure what to return



# Create your models here.
class Incident(models.Model):
	priority = models.IntegerField()
	is_resolved = models.BooleanField(default=False)
	category = models.CharField(max_length= 30)
	location = models.CharField(max_length= 250)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
    objects = IncidentManager()

class Call(models.Model):
	raw_text = models.TextField()
	parsed_text = models.TextField()
	location = models.CharField(max_length= 250)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	incident_id = models.ForeignKey(Incident, related_name="calls")
