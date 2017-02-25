import json

import random
from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):

    return render(request, 'disaster_dispatch/index.html')

def refresh(request):
    response_data = {}
    response_data['result'] = "DUMMY TEXT"
    response_data['message'] = "DUMMY MESSAGE"
    response_data['random'] = random.choice("HELLO_piZZza")
    return HttpResponse(json.dumps(response_data), content_type="application/json")
