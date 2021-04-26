from django.urls import path,include
from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

app_name='main'

urlpatterns = [
    path('',views.homepage,name="homepage"),
    path('registry/',views.registry,name="registry"),
    path('registry/<str:id>/', views.patientsentry, name="patientsentry"),
    path('registry/<str:id>/<str:sid>',views.caseentry,name="caseentry"),
    path('allcases',views.allcases,name="allcases"),
    path('patientform/',views.createPatient, name="patientform"),
    path('patientform/update/<str:id>',views.updatePatient, name="update_patientform"),
    path('patientform/delete/<str:id>',views.deletePatient, name="delete_patient"),
    path('caseform/',views.createCase, name="caseform"),
    path('patientcaseform/<str:id>',views.createCasefromPatient, name="patientcaseform"),
    path('caseform/update/<str:sid>',views.updateCase, name="update_caseform"),
    path('caseform/delete/<str:sid>',views.deleteCase, name="delete_caseform"),
    path('adminregistry/',views.adminregistry,name="adminregistry"),
    path('adminallcases/',views.adminallcases,name="adminallcases"),
    path('adminusers/',views.adminusers,name="adminusers"),
    path('adddoctor/<str:id>',views.addgrouptouser,name="addgrouptouser"),
    path('removedoctor/<str:id>',views.removegrouptouser,name="removegrouptouser"),
    path('denyapplication/<str:id>',views.denyapplication,name="denyapplication"),
    path('profile/',views.profile,name="profile"),
    path('pdf/<str:id>/<str:sid>',views.render_pdf_view,name="pdf"),
    path('regmailpatient/',views.email_reg_patient,name="emailreg"),
    path('doctorformauth/',views.doctor_form_submit,name="docformsubmit"),



]
