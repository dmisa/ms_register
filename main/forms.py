from django.forms import ModelForm
from .models import *

class MspatientForm(ModelForm):
    class Meta:
        model=Mspatient
        fields = '__all__'
