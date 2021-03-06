from django.urls import path,include
from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

app_name='main'

urlpatterns = [
    path("",views.homepage,name="homepage"),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    path("registry",views.registry,name="registry"),
    path("registry/<str:pk>/",views.registry,name="registry"),


]