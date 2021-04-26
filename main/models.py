from django.db import models
from django.db.models import IntegerField, DateField,TimeField, BooleanField,CharField, Model
from users.models import User

class DoctorApplication(models.Model):
    user=models.ForeignKey(User,editable=False, null=True,blank=True, on_delete= models.SET_NULL)
    datecreated = models.DateField(auto_now_add=True)
    approved=models.BooleanField(default=False)
    reviewed=models.BooleanField(default=False)

class Mspatient(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30,default='')
    address = models.CharField(max_length=30)
    datecreated = models.DateField(auto_now_add=True)
    createdby = models.ForeignKey(User,editable=False, null=True,blank=True, on_delete= models.SET_NULL)
    def __str__(self):
        return '%s %s' % (self.name,self.surname)

class Mscase(models.Model):
    ms_choices=(
        ('RR','Relapsing-remitting MS'),
        ('SP','Secondary progressive MS'),
        ('PP','Primary progressive MS'),
        ('Other','Other'),
    )

    severity_choices=(
        ('Mild','Mild'),
        ('Moderate','Moderate'),
        ('Severe','Severe'),
    )
    modtreat_choices=(
        ('Alemtuzumab','Alemtuzumab'),
        ('Avonex','Avonex'),
        ('Betaferon','Betaferon'),
        ('Copaxone','Copaxone'),
        ('Extavia','Extavia'),
        ('Fingolimod','Fingolimod'),
        ('Mitoxantrone','Mitoxantrone'),
        ('Natalizumab','Natalizumab'),
        ('Ocrelizumab','Ocrelizumab'),
        ('Rebif','Rebif'),
        ('Tecfidera','Tecfidera'),
        ('Teriflunomide','Teriflunomide'),
        ('None','None'),
    )
    pastmodreason_choices=(
        ('Lack of efficacy','Lack of efficacy'),
        ('Side Effects','Side Effects'),
        ('Other','Other'),
    )
    evaluation_choices=(
        ('Self-estimated','Self-estimated'),
        ('Trundle wheel','Trundle wheel'),
        ('Treadmill','Treadmill'),        
    )

    onsetlocal_choices=(
        ('Spinal','Spinal'),
        ('Cortex','Cortex'),
        ('Visual','Visual'),
        ('Cerebellar/brainstem','Cerebellar/brainstem'),
    )

    onsetsympt_choices=(
        ('Vision','Vision'),
        ('Motor','Motor'),
        ('Sensory','Sensory'),
        ('Coordination','Coordination'),
        ('Bowel/Bladder','Bowel/Bladder'),
        ('Fatigue','Fatigue'),
        ('Cognitive','Cognitive'),
        ('Encephalopathy','Encephalopathy'),
        ('Other','Other'),        
    )
    yes_no=(
        ('Yes','Yes'),
        ('No','No')
    )
    mspatient = models.ForeignKey(Mspatient, null=True, on_delete= models.CASCADE)
    formdate = models.DateField()
    studyid = models.CharField(max_length=6,primary_key=True)

    ms_now = models.CharField(max_length=10,choices=ms_choices)
    conv_to_sp=models.CharField(max_length=20)
    date_diag=models.DateField()
    ms_diag= models.CharField(max_length=10,choices=ms_choices)
    date_onset=models.DateField()
    num_relapses=IntegerField()
    severity=models.CharField(max_length=10,choices=severity_choices)
    pastmodtreat=models.CharField(max_length=20,choices=modtreat_choices)
    pastmoddatestart=models.DateField()
    pastmodtreatstop=models.DateField()
    pastmodreason= models.CharField(max_length=20,choices=pastmodreason_choices)
    presmodtreat=models.CharField(max_length=20,choices=modtreat_choices)
    presmoddatestart=models.DateField()
    edssscore=IntegerField()
    edssdate=DateField()
    walkrangetime=CharField(max_length=5)
    walkrangedist=IntegerField()
    walkrangeeval=models.CharField(max_length=20,choices=evaluation_choices)


    pregnant=models.CharField(max_length=20,choices=yes_no,null=True,blank=True)
    smoker=models.CharField(max_length=20,choices=yes_no,null=True,blank=True)
    cigperday=IntegerField(null=True,blank=True)
    smokersince=IntegerField(null=True,blank=True)
    onsetlocal = models.CharField(max_length=30,choices=onsetlocal_choices,null=True,blank=True)
    onsetsympt = models.CharField(max_length=30,choices=onsetsympt_choices,null=True,blank=True)

    comorbidities=models.CharField(max_length=20,choices=yes_no,null=True,blank=True)
    ethnicity=models.CharField(max_length=20,null=True,blank=True)
    age=IntegerField(null=True,blank=True)
    race=models.CharField(max_length=20,null=True,blank=True)
    

    personcompleting=models.ForeignKey(User,editable=False, null=True, on_delete= models.CASCADE)
    def __str__(self):
        return 'Case #%s' % (self.studyid)
