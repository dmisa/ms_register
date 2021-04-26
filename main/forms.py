from .models import *
from allauth.account.forms import SignupForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.shortcuts import redirect

class DateInput(forms.DateInput):
    input_type = 'date'

class MscaseForm(ModelForm):
    def save(self, user = None, force_insert = False, force_update = False, commit = True):
        cas= super(MscaseForm,self).save(commit=False)
        cas.personcompleting=user
        if commit:
            cas.save()
        return cas
    class Meta:
        model=Mscase
        fields = '__all__' 
        exclude = ('personcompleting',)

        widgets = {
            'mspatient': forms.Select(attrs={'class':'form-control'}),
            'formdate': DateInput(attrs={'class':'form-control'}),
            'studyid':forms.TextInput(attrs={'class':'form-control'}),

            #tier one
            'ms_now':forms.Select(attrs={'class':'form-control'}),
            'conv_to_sp':forms.TextInput(attrs={'class':'form-control'}),
            'date_diag': DateInput(attrs={'class':'form-control'}),
            'ms_diag':forms.Select(attrs={'class':'form-control'}),
            'date_onset':DateInput(attrs={'class':'form-control'}),
            'num_relapses':forms.TextInput(attrs={'class':'form-control'}),
            'severity':forms.Select(attrs={'class':'form-control'}),
            'pastmodtreat':forms.Select(attrs={'class':'form-control'}),
            'pastmoddatestart':DateInput(attrs={'class':'form-control'}),
            'pastmodtreatstop':DateInput(attrs={'class':'form-control'}),
            'pastmodreason':forms.Select(attrs={'class':'form-control'}),

            'presmodtreat':forms.Select(attrs={'class':'form-control'}),
            'presmoddatestart':DateInput(attrs={'class':'form-control'}),
            'edssscore':forms.TextInput(attrs={'class':'form-control'}),
            'edssdate':DateInput(attrs={'class':'form-control'}),
            'walkrangetime':forms.TextInput(attrs={'class':'html-duration-picker form-control','data-hide-seconds':''}),
            'walkrangedist':forms.TextInput(attrs={'class':'form-control'}),
            'walkrangeeval':forms.Select(attrs={'class':'form-control'}),
            #tier two
            'pregnant':forms.Select(attrs={'class':'form-control novalidate'}),
            'smoker':forms.Select(attrs={'class':'form-control novalidate'}),
            'cigperday':forms.TextInput(attrs={'class':'form-control novalidate'}),
            'smokersince':forms.TextInput(attrs={'class':'form-control novalidate'}),    
            'onsetlocal':forms.Select(attrs={'class':'form-control novalidate'}),
            'onsetsympt':forms.Select(attrs={'class':'form-control novalidate'}),
            #tier three
            'comorbidities':forms.Select(attrs={'class':'form-control novalidate'}),
            'ethnicity':forms.TextInput(attrs={'class':'form-control novalidate'}),  
            'age':forms.TextInput(attrs={'class':'form-control novalidate'}),  
            'race':forms.TextInput(attrs={'class':'form-control novalidate'}),  
            
        }
    def __init__(self, user=None, *args, **kwargs):
        super(MscaseForm, self).__init__(*args,**kwargs)
        self.fields['mspatient'].queryset = Mspatient.objects.filter(createdby=user)




class MspatientForm(ModelForm):
    def save(self, user = None, force_insert = False, force_update = False, commit = True):
        pat= super(MspatientForm,self).save(commit=False)
        pat.createdby=user
        if commit:
            pat.save()
        return pat
    class Meta:
        model = Mspatient
        fields = '__all__'
        exclude = ('createdby',)

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'surname':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
        }



class DoctorApplicationForm(ModelForm):
    def save(self, user = None, force_insert = False, force_update = False, commit = True):
        app= super(DoctorApplicationForm,self).save(commit=False)
        app.user=user
        if commit:
            app.save()
        return app
    class Meta:
        model = DoctorApplication
        exclude=('__all__')



class MyCustomSignupForm(SignupForm):
    name = forms.CharField(max_length=30, label='Name')
    surname = forms.CharField(max_length=30, label='Surname')
    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.surname = self.cleaned_data['surname']
        user.save()
        return user


class addgroupstouser(ModelForm):
    class Meta:
        model= User
        fields=('groups',)

