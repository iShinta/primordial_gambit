import json
import random
from django.shortcuts import render, HttpResponse
from .models import Incident, Call
import imaplib
import string
from django.core import serializers


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
    if request.method == "POST":
        pk = request.POST.pk
        Incident.objects.get(pk=pk).update(is_resolved=True)
    return redirect("/")

def show(request, id):
    context_object = {}
    context_object['incident'] = Incident.objects.get(pk=id)
    context_object['calls'] = Call.objects.filter(incident=context_object['incident'])
    return render(request, 'disaster_dispatch/show.html', context_object)
