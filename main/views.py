from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *

def homepage(request):
    return render(request,
                  template_name='main/home.html')



def registry(request):
    mspatients = Mspatient.objects.all()
    return render(request, 'main/registry.html', {'mspatients':mspatients})

def registryentry(request,sid):
    mspatient = Mspatient.objects.get(studyid=sid)

    return render(request, 'main/patient.html', {'mspatient':mspatient})

def createCase(request):
    form=MspatientForm()
    if request.method =='POST':
        form=MspatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context={'form':form}
    return render(request,'main/patientform.html',context)

def updateCase(request, sid):
    mspatient=Mspatient.objects.get(studyid=sid)
    form=MspatientForm(instance=mspatient)
    if request.method =='POST':
        form=MspatientForm(request.POST, instance=mspatient)
        if form.is_valid():
            form.save()
            return redirect('/')    
    context={'form':form}
    return render(request,'main/patientform.html',context)

def deleteCase(request,sid):
    mspatient=Mspatient.objects.get(studyid=sid)
    if request.method == "POST":
        mspatient.delete()
        return redirect('/')    

    context={'item':mspatient}
    return render(request,'main/delete.html',context)