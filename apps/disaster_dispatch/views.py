import json
import random
from django.shortcuts import render, HttpResponse, redirect
from .models import Incident, Call
import imaplib
import string
from django.core import serializers
import requests
import geocoder


# Create your views here.

def index(request):
    return render(request, 'disaster_dispatch/index.html')

def refresh(request):
    raw_text = read()
    if len(raw_text) > 0:
        for text in raw_text:
            Incident.objects.parse_text(text.translate(None, string.punctuation))
    all_incidents = Incident.objects.filter(is_resolved=False).order_by('priority')
    all_incidents = serializers.serialize('json',all_incidents)
    return HttpResponse(json.dumps(all_incidents), content_type="application/json")
# def index(request):
#     raw_text = read()
#     if len(raw_text) > 0:
#         for text in raw_text:
#             Incident.objects.parse_text(text.translate(None, string.punctuation))
#     all_incidents = Incident.objects.filter(is_resolved=False).order_by('priority')
#     # all_incidents = serializers.serialize('json',all_incidents)
#
#     context_dictionary = {}
#     context_dictionary['incidents'] = []
#
#     for incident in all_incidents:
        # if not incident.location == "":
        #   try:
        #     #   location_instance = incident.location
        #       mapsURI = 'https://maps.googleapis.com/maps/api/geocode/json'
        #       raw_coord =  incident.location.replace("[","").replace("]","").replace(" ", "")
        #       api_key = "AIzaSyBvFTtUMAzs2aGJ_PWUNVWZrehCo0VADo0"
          #
        #       payload = {
        #         'latlng': coord,
        #         'key': api_key
        #       }
          #
        #       full_uri = mapsURI+"?latlng="+coord+"&key="+api_key
        #       print ("coord: ", coord)
          #
        #     #   print ("prelatlng: ", float(location[1]))
        #     #   trimmed = incident.location[1:len(incident.location)-1]
        #     #   separated = trimmed.split(", ")
        #     #   for i in range(len(location)):
        #     #       if location[i][0] == "-":
        #     #           location[i] = float(location[1:])
        #     #           print ("un: ", location[i])
        #     #       else:
        #     #           location[i] = float(location)
        #     #           print ("do: ", location[i])
          #
        #     #   print ("latlng: ", location)
          #
        #       results = requests.get(full_uri).json()
        #       print results
        #       location = "unknown"
        #     #   geolocation = geocoder.google(location, method="reverse")
        #     #   print geolocation.city
        #   except:
        #       location = "unknown"
    #
    #     incidents_dict = {
    #         "pk" : incident.pk,
    #         "priority": incident.priority,
    #         "location": incident.location,
    #         "address" : incident.address,
    #         "category": incident.category,
    #         "people": incident.people,
    #         "created_at": incident.created_at
    #     }
    #
    #     context_dictionary['incidents'].append(incidents_dict)
    # return render(request, 'disaster_dispatch/index.html', context_dictionary)

# def refresh(request):
#     raw_text = read()
#     if len(raw_text) > 0:
#         for text in raw_text:
#             Incident.objects.parse_text(text.translate(None, string.punctuation))
#     all_incidents = Incident.objects.filter(is_resolved=False).order_by('priority')
#     # all_incidents = serializers.serialize('json',all_incidents)
#
#     incidents_output = []
#
#     for incident in all_incidents:
#         incidents_dict = {
#             "pk" : incident.pk,
#             "priority": incident.priority,
#             "location": incident.location,
#             "category": incident.category,
#             "people": incident.people,
#             "created_at": incident.created_at
#         }
#
#         incidents_output.append(incidents_dict)
#     return HttpResponse(json.dumps(all_incidents), content_type="application/json")


def read():
	imap = imaplib.IMAP4_SSL('imap.gmail.com')
	imap.login('primordialgambit@gmail.com', 'md5hackathon')
	imap.select('INBOX')
	status, response = imap.search(None, '(UNSEEN)', '(FROM "Google Voice")')
	unread_msg_nums = response[0].split()
	da = []
	if status == "OK":
		for e_id in unread_msg_nums:
			_, response = imap.fetch(e_id, '(RFC822)')
			start = "<https://www.google.com/voice/>"
			end = "play message"
			res = response[0][1]
			da.append(res[res.find(start)+len(start):res.find(end)].replace("\r\n",''))
	return da

def resolve_incident(request):
    print '0000000000000000000000' , request.POST
    if request.method == "POST":
        pk = request.POST['pk']
        Incident.objects.filter(pk=pk).update(is_resolved=True)
    return redirect("/")

def show(request, id):
    context_object = {}
    context_object['incident'] = Incident.objects.get(pk=id)
    context_object['calls'] = Call.objects.filter(incident=context_object['incident'])
    return render(request, 'disaster_dispatch/show.html', context_object)
