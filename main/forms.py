from django.forms import ModelForm
from .models import *

class MscaseForm(ModelForm):
    class Meta:
        model=Mscase
        fields = '__all__'
