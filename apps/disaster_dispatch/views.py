import json
import random
from django.shortcuts import render, HttpResponse
from ..ml.models import Incident, Call
from ..ml import views as mlViews

# Create your views here.
def index(request):
    return render(request, 'disaster_dispatch/index.html')

def refresh(request):
    raw_text = mlViews.read()
    print '*' * 100
    print raw_text
    if len(raw_text) >= 0:
        incident = Incident.objects.parse_text(raw_text)
    all_incidents = Incident.objects.filter(is_resolved="False").order_by(priority)
    return HttpResponse(json.dumps(response_data), content_type="application/json")
