from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *

def homepage(request):
    return render(request,
                  template_name='main/home.html')



def registry(request):
    mscases = Mscase.objects.all()
    return render(request, 'main/registry.html', {'mscases':mscases})

def registryentry(request,sid):
    mscase = Mscase.objects.get(studyid=sid)

    return render(request, 'main/case.html', {'mscase':mscase})

def createCase(request):
    form=MscaseForm()
    if request.method =='POST':
        form=MscaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context={'form':form}
    return render(request,'main/caseform.html',context)

def updateCase(request, sid):
    mscase=Mscase.objects.get(studyid=sid)
    form=MscaseForm(instance=mscase)
    if request.method =='POST':
        form=MscaseForm(request.POST, instance=mscase)
        if form.is_valid():
            form.save()
            return redirect('/')    
    context={'form':form}
    return render(request,'main/caseform.html',context)

def deleteCase(request,sid):
    mscase=Mscase.objects.get(studyid=sid)
    if request.method == "POST":
        mscase.delete()
        return redirect('/')    

    context={'item':mscase}
    return render(request,'main/deletecase.html',context)