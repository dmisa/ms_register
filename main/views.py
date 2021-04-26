from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.decorators import login_required
from .decorators import *
from django import forms,template
from django.contrib import messages
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.db.models import Avg,Count
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage

def homepage(request):
    if request.user.is_authenticated:
        allowed_groups=['admin','doctor']
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
            if group in allowed_groups:
                DoctorApplication.objects.filter(user=request.user).delete()
                labelsmsnow = []
                datamsnow = []
                labelssev = []
                datasev = []
                mscases = Mscase.objects.filter(personcompleting=request.user.id)
                mspatients= Mspatient.objects.filter(createdby=request.user)
                last_5_mspatients=Mspatient.objects.filter(createdby=request.user).order_by('-datecreated')[:5]
                last_5_mscases = Mscase.objects.filter(personcompleting=request.user.id).order_by('-formdate')[:5]

                total_patients=mspatients.count()
                total_cases=mscases.count()
                average_age=mscases.aggregate(Avg('age'))
                average_age=average_age.get('age__avg')

                queryset=Mscase.objects.filter(personcompleting=request.user.id).values('ms_now').annotate(total=Count('ms_now')).order_by('total')
                for entry in queryset:
                    labelsmsnow.append(entry['ms_now'])
                    datamsnow.append(entry['total'])
        
                queryset=Mscase.objects.filter(personcompleting=request.user.id).values('severity').annotate(total=Count('severity')).order_by('total')
                for entry in queryset:
                    labelssev.append(entry['severity'])
                    datasev.append(entry['total'])

                context = {'mscases':mscases, 'mspatients':mspatients,
                'total_cases':total_cases,'total_patients':total_patients,
                'average_age':average_age,'datamsnow':datamsnow,'labelsmsnow':labelsmsnow,'datasev':datasev,'labelssev':labelssev,
                'last_5_mspatients':last_5_mspatients,'last_5_mscases':last_5_mscases}


                return render(request,'main/dashboard.html', context)
            else:
                doctorapplications=DoctorApplication.objects.filter(user=request.user)
                if doctorapplications:
                    k=0
                    for doctorapplication in doctorapplications:
                        if k>=4:
                            doctorapplication.delete()
                        k+=1
                doctorapplication= DoctorApplication.objects.filter(user=request.user).last()
                if doctorapplication:
                    return render(request, 'main/info.html',{'doctorapplication':doctorapplication})
                else:
                    return render(request, 'main/info.html')

        else:
                doctorapplications=DoctorApplication.objects.filter(user=request.user)
                if doctorapplications:
                    k=0
                    for doctorapplication in doctorapplications:
                        if k>=4:
                            doctorapplication.delete()
                        k+=1
                doctorapplication= DoctorApplication.objects.filter(user=request.user).last()
                if doctorapplication:
                    return render(request, 'main/info.html',{'doctorapplication':doctorapplication})
                else:
                    return render(request, 'main/info.html')
    else:
        return render(request,'main/home.html')

@login_required
@allowed_users(allowed_roles=['admin','doctor'])
def registry(request):
    search_patient = request.GET.get('search')
    if search_patient:
        mspatients= Mspatient.objects.filter(createdby=request.user)
        for term in search_patient.split():
            mspatients = mspatients.filter( Q(name__icontains = term) | Q(surname__icontains = term) | Q(id__icontains = term))    
    else:
        mspatients= Mspatient.objects.filter(createdby=request.user)
    mscases = Mscase.objects.filter(personcompleting=request.user.id)
    thefilter=MspatientFilter(request.GET,queryset=mspatients)
    mspatients=thefilter.qs
    return render(request, 'main/registry.html', {'mspatients':mspatients, 'mscases':mscases,'thefilter':thefilter})



@login_required
@allowed_users(allowed_roles=['admin','doctor'])
def allcases(request):
    mspatients= Mspatient.objects.filter(createdby=request.user)
    mscases = Mscase.objects.filter(personcompleting=request.user.id)
    
    thefilter=MscaseFilter(request.GET,queryset=mscases,request=request)
    
    mscases=thefilter.qs
    return render(request, 'main/allcases.html', {'mspatients':mspatients, 'mscases':mscases,'thefilter':thefilter})

@allowed_users(allowed_roles=['admin','doctor'])
def patientsentry(request,id):
    mspatient = Mspatient.objects.get(id=id)
    mscases = mspatient.mscase_set.all()
    return render(request, 'main/patient.html', {'mspatient':mspatient,'mscases':mscases,'id':id})

@allowed_users(allowed_roles=['admin','doctor'])
def caseentry(request,id,sid):
    mspatient = Mspatient.objects.get(id=id)
    mscase=Mscase.objects.get(studyid=sid)
    return render(request, 'main/case.html', {'mspatient':mspatient,'mscase':mscase})

@allowed_users(allowed_roles=['admin','doctor'])
def createPatient(request):
    form=MspatientForm()
    if request.method =='POST':
        form=MspatientForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request,'You successfully created a patient')
            return redirect('/registry')
        
    context={'form':form}
    return render(request,'main/patientform.html',context)

@allowed_users(allowed_roles=['admin','doctor'])
def createCase(request):
    form=MscaseForm()
    if request.method =='POST':
        form=MscaseForm(request.user,request.POST)
        if form.is_valid():
            mscase=form.save(user=request.user,commit=False)
            messages.success(request,'You successfully created a case')
            mscase.user = request.user
            mscase.save()
            return redirect('/allcases')
    else:
        form = MscaseForm(request.user)        
    context={'form':form}
    return render(request,'main/caseform.html',context)

@allowed_users(allowed_roles=['admin','doctor'])
def createCasefromPatient(request,id):
    mspatient=Mspatient.objects.get(id=id)
    form=MscaseForm(initial={'mspatient':mspatient})
    if request.method =='POST':
        form=MscaseForm(request.user,request.POST,initial={'mspatient':mspatient})
        if form.is_valid():
            mscase=form.save(user=request.user,commit=False)
            mscase.user = request.user
            mscase.save()
            return redirect('/allcases')
    else:
        form = MscaseForm(request.user,initial={'mspatient':mspatient})        
    context={'form':form,'mspatient':mspatient}
    return render(request,'main/caseformfrompatient.html',context)



@allowed_users(allowed_roles=['admin','doctor'])
def updateCase(request, sid):
    mscase=Mscase.objects.get(studyid=sid)
    form=MscaseForm(request.user,instance=mscase)
    if request.method =='POST':
        form=MscaseForm(request.user,request.POST, instance=mscase)
        if form.is_valid():
            mscase=form.save(user=request.user,commit=False)
            mscase.user = request.user
            mscase.save()
            return redirect('/allcases') 
            messages.success(request,'You successfully updated a case')

    context={'form':form}
    return render(request,'main/caseeditform.html',context)


@allowed_users(allowed_roles=['admin','doctor'])
def deleteCase(request,sid):
    mscase=Mscase.objects.get(studyid=sid)
    if request.method == "POST":
        mscase.delete()
        messages.success(request,'Case Deleted')
        return redirect('/allcases')    



@allowed_users(allowed_roles=['admin','doctor'])
def updatePatient(request, id):
    mspatient=Mspatient.objects.get(id=id)
    form=MspatientForm(instance=mspatient)
    if request.method =='POST':
        form=MspatientForm(request.POST, instance=mspatient)
        if form.is_valid():
            form.save(user=mspatient.createdby)
            return redirect('/registry')
            messages.success(request, 'Patient Updated')
    context={'form':form,'mspatient':mspatient}
    return render(request,'main/patienteditform.html',context)

@allowed_users(allowed_roles=['admin','doctor'])
def deletePatient(request,id):
    mspatient=Mspatient.objects.get(id=id)
    if request.method == "POST":
        mspatient.delete()
        messages.success(request,'Patient Deleted')
        return redirect("/registry")    

@allowed_users(allowed_roles=['admin','doctor'])
def email_reg_patient(request):
    if request.method=='POST':
        from_email = 'testmsreg@gmail.com'
        rec=request.POST.get("patientmail")
        recipient_list = [rec,]
        subject="Invitation to register (MSREGISTRY)"
        message = render_to_string('account/email/patientsubscribe.txt')
        mail=send_mail(subject, message, from_email, recipient_list)
        if mail:
            messages.success(request, 'Email has been sent.')
            return redirect('/caseform')    
    else:
        return render(request,'main/patientregistration.html')








@login_required
@allowed_users(allowed_roles=['admin'])
def adminregistry(request):
    mscases = Mscase.objects.all()
    mspatients= Mspatient.objects.all()

    return render(request, 'main/admin/adminregistry.html', {'mspatients':mspatients, 'mscases':mscases})


@login_required
@allowed_users(allowed_roles=['admin'])
def adminallcases(request):
    mscases = Mscase.objects.all()
    mspatients= Mspatient.objects.all()
   
    thefilter=MscaseFilter(request.GET,queryset=mscases,request=request)
    
    mscases=thefilter.qs
    return render(request, 'main/admin/adminallcases.html', {'mspatients':mspatients, 'mscases':mscases,'thefilter':thefilter})




@login_required
@allowed_users(allowed_roles=['admin'])
def adminusers(request):
    users=User.objects.filter(~Q(id=request.user.id))
    apps=DoctorApplication.objects.all()
    return render(request, 'main/admin/adminusers.html', {'users':users,'apps':apps} )

@login_required
@allowed_users(allowed_roles=['admin'])
def addgrouptouser(request,id):
    user=User.objects.get(id=id)
    
    my_group = Group.objects.get(name='doctor') 
    my_group.user_set.add(user)
    from_email = 'testmsreg@gmail.com'
    rec=user.email
    recipient_list = [rec,]
    subject="You are officialy an MS Doctor "+request.user.email
    message="Your application is approved. You can now use the application"
    mail=send_mail(subject, message, from_email, recipient_list)
    if mail:
        messages.success(request, 'You succesfully added a doctor')
        app=DoctorApplication.objects.filter(user=user).last()
        app.approved=True
        app.reviewed=True
        app.save()
        DoctorApplication.objects.filter(user=user).delete()

    return redirect('/adminusers')    


@login_required
@allowed_users(allowed_roles=['admin'])
def denyapplication(request,id):
    user=User.objects.get(id=id)
    from_email = 'testmsreg@gmail.com'
    rec=user.email
    recipient_list = [rec,]
    subject="Your application is denied!"+user.email
    message="Your application is denied. You are not a verified doctor."
    mail=send_mail(subject, message, from_email, recipient_list)
    application=DoctorApplication.objects.filter(user=user).last()
    application.approved=False
    application.reviewed=True

    if mail:
        messages.success(request, 'You succesfully denied an application')
    return redirect('/adminusers')  

@login_required
@allowed_users(allowed_roles=['admin'])
def removegrouptouser(request,id):
    user=User.objects.get(id=id)
    my_group = Group.objects.get(name='doctor') 
    my_group.user_set.remove(user)

    from_email = 'testmsreg@gmail.com'
    rec=user.email
    recipient_list = [rec,]
    subject="Removed from MS Registry "+user.email
    message="You have been removed from MSREGISTRY. You cannot use the application anymore."
    mail=send_mail(subject, message, from_email, recipient_list)
    if mail:
        messages.success(request, 'You succesfully removed a doctor')

    return redirect('/adminusers')    

@login_required
def profile(request):
    return render(request, 'account/base.html' )

@login_required
@allowed_users(allowed_roles=['admin','doctor'])
def render_pdf_view(request,id):
    template_path = 'main/pdf.html'
    mscase=Mscase.objects.get(studyid=id)

    context = {'mscase': mscase}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def doctor_form_submit(request):
    if request.method =='POST':
        form=DoctorApplicationForm(request.POST)
        form.save(user=request.user)
        from_email = request.user.email
        rec='testmsreg@gmail.com'
        recipient_list = [rec,]
        subject="Authorize me as doctor "+request.user.email
        message=request.POST.get('message')+"<br>"+request.user.email
        email=EmailMessage(subject,message,from_email,recipient_list)
        email.content_subtype = 'html'

        file = request.FILES['file']
        email.attach(file.name, file.read(), file.content_type)
        email.send()
        if email:
            from_email = 'testmsreg@gmail.com'
            rec=request.user.email
            recipient_list = [rec,]
            subject="(CONFIRMATION) AUTHORIZATION IN PROGRESS"
            message = "we will let you know soon"
            mail=send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Email has been sent.')
            return redirect('/')  



