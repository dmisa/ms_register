import django_filters
from django_filters import DateFilter
from .models import *

def filtered_queryset(request):
    return Mspatient.objects.filter(createdby=request.user)

class MscaseFilter(django_filters.FilterSet):
    s_d=DateFilter(field_name="formdate",lookup_expr='gte')
    e_d=DateFilter(field_name="formdate",lookup_expr='lte')
    a_gt=django_filters.NumberFilter(field_name='age', lookup_expr='gt')

    mspatient=django_filters.ModelChoiceFilter(queryset=filtered_queryset)
    class Meta:
        model= Mscase
        fields = ['mspatient','studyid','ms_now']



class MspatientFilter(django_filters.FilterSet):
    class Meta:
        model= Mspatient
        fields = '__all__'

