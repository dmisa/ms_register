from django.urls import path,include
from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

app_name='main'

urlpatterns = [
    path('',views.homepage,name="homepage"),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    path('registry/',views.registry,name="registry"),
    path('registry/<str:sid>/', views.registryentry, name="registryentry"),
    path('caseform/',views.createCase, name="caseform"),
    path('caseform/update/<str:sid>',views.updateCase, name="update_caseform"),
    path('caseform/delete/<str:sid>',views.deleteCase, name="delete_caseform"),

]