from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def homepage(request):
    return render(request,
                  template_name='main/home.html')


def registry(request):
    mspatients = mspatient.objects.all()
    return render(request, 'main/registry.html', {'mspatients':mspatients})

def registry(request,pk):
    mspatients = mspatient.objects.get(id=pk)
    return render(request, 'main/patient.html', {'mspatients':mspatients})