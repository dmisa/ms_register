from django.db import models
from django.db.models import IntegerField, DateField,TimeField, BooleanField,CharField, Model

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
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30,default='')
    address = models.CharField(max_length=30)
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
    walkrangetime=TimeField()
    walkrangedist=IntegerField()
    walkrangeeval=models.CharField(max_length=20,choices=evaluation_choices)


    pregnant=BooleanField(null=True)
    smoker=BooleanField(null=True)
    cigperday=IntegerField(null=True)
    smokersince=IntegerField(null=True)
    onsetlocal = models.CharField(max_length=30,choices=onsetlocal_choices,null=True)
    onsetsympt = models.CharField(max_length=30,choices=onsetsympt_choices,null=True)
    personcompleting=CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return (self.studyid + 'of patient' + self.name + self.surname)