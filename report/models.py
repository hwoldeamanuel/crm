from django.db import models
from program.models import  Program, Indicator, UserRoles
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_delete,pre_save
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone
import os
from django.db.models import Max, Avg,Sum,Count,F
from uuid import uuid4
# Create your models here.
from app_admin.models import Country as NCountry, Region as NRegion, Zone as NZone, Woreda as NWoreda, Submission_Status, Approvalf_Status,Approvalt_Status
from django.contrib.auth.models import User
from portfolio.models import Portfolio
from conceptnote.models import Icn, Activity, Impact, ActivityImpact
from program.models import ImplementationArea
from django.core.validators import FileExtensionValidator

class IcnReport(models.Model):
    icn = models.OneToOneField(Icn, on_delete=models.DO_NOTHING, related_name='icnreport')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    actual_start_date = models.DateField()
    actual_end_date = models.DateField()
    
    ilead_agency = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='ricns')
    ilead_co_agency = models.ManyToManyField(Portfolio,  blank=True, related_name='rco_leads')
    actual_report_date = models.DateField(null=True, blank=True)
    program_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='irprogram_lead')
    technical_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='irtechnical_lead')
    mel_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='irmel_lead')
    finance_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='irfinance_lead')
    description = models.TextField(null=True, blank=True)
    iworeda = models.ManyToManyField(ImplementationArea,  blank=True, related_name='program_rworedas')
    
    actual_mc_budget= models.FloatField(null=True, blank=True)
    
    actual_cost_sharing_budget = models.FloatField(null=True, blank=True)
    USD = 1
    ETB = 2
    CURRENCY_CHOICES =   (
        (USD, '$'),
        (ETB, 'Br'),
     
        )

 
    mc_currency = models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES, default = 1, blank=True, null=True)
    cs_currency =  models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES, default = 1, blank=True, null=True)
   
   

    STATUS_CHOICES = [(False, 'Draft'), (True, 'Submitted')]
    status = models.BooleanField("Status", default=False, 
                                       choices=STATUS_CHOICES)
    approval_status = models.CharField(max_length=100,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def get_name(self):
        return "InterventionReport"
    
    def __str__(self):
        return str(self.icn.title)
  

class IcnReportImplementationArea(models.Model):
    icnreport =  models.ForeignKey(
        IcnReport, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(
        NRegion, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(
        NZone, on_delete=models.CASCADE, null=True, blank=True)
    woreda = models.OneToOneField(NWoreda, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

def path_and_rename(instance, filename):
    upload_to = 'Report/'
    ext = filename.split('.')[-1]

    # get filename
    if hasattr(instance, 'icnreport'):
        filename = '{}.{}'.format(instance.icnreport.icn.title +"_Version_"+ instance.ver + "_" + instance.user.username + "_" + timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M:%S'), ext)
    elif hasattr(instance, 'activityreport'):
         filename = '{}.{}'.format(instance.activityreport.activity.title +"_Version_"+ instance.ver + "_" + instance.user.username + "_" + timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M:%S'), ext)
        # set filename as random string
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
    

class IcnReportDocument(models.Model):
    user = models.ForeignKey(User, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='icnreportuploaded_by')
    icnreport = models.ForeignKey(IcnReport, on_delete=models.CASCADE, default=2,  blank=True)
    description = models.TextField(blank=True, null=True)
    document = models.FileField(null=True,  blank=True, max_length=500, upload_to=path_and_rename, validators=[FileExtensionValidator(allowed_extensions=["doc","docx","pdf" ])])
    ver = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,  null=True,  blank=True)

    class Meta:
        ordering = ('-uploaded_at',)
    
    
    
    def __str__(self):
        return "%s %s %s" % ("Version", self.ver, self.user.username)
    
      

    
    
    

class IcnReportSubmit(models.Model):

    id = models.AutoField(primary_key=True)
    icnreport =  models.ForeignKey(
        IcnReport, on_delete=models.CASCADE, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    submission_status = models.ForeignKey(Submission_Status, on_delete=models.CASCADE)
    submission_note = models.TextField(null=True,  blank=True)

    document = models.ForeignKey(IcnReportDocument, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ('-submission_date',)
    
    
    def save(self, *args, **kwargs):
        if self.submission_date and self.old_submission_date != self.submission_date:
            self.submission_date = timezone.now()
        super(IcnReportSubmit, self).save(*args, **kwargs)
   
    
    def __str__(self):
        return str(self.id)
    



class IcnReportSubmitApproval_T(models.Model):
        
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(IcnReportSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(IcnReportDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(IcnReportSubmitApproval_T, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(IcnReportSubmitApproval_T, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)

class IcnReportSubmitApproval_M(models.Model):
        
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(IcnReportSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(IcnReportDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(IcnReportSubmitApproval_M, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(IcnReportSubmitApproval_M, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)
    
    

class IcnReportSubmitApproval_P(models.Model):
  
    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(IcnReportSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalf_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(IcnReportDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(IcnReportSubmitApproval_P, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(IcnReportSubmitApproval_P, self).save(*args, **kwargs)

 
        
    def __str__(self):
        return str(self.id)

class IcnReportSubmitApproval_F(models.Model):

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(IcnReportSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(IcnReportDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(IcnReportSubmitApproval_F, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(IcnReportSubmitApproval_F, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.id)
    


class IcnReportImpact(models.Model):
    icnreport =  models.ForeignKey(
        IcnReport, on_delete=models.CASCADE, null=True, blank=True)
    impact = models.OneToOneField(Impact, on_delete=models.CASCADE, null=True, blank=True)
    
    actual_impact_pilot  = models.FloatField(null=True, blank=True)
    actual_impact_scaleup  = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return str(self.icnreport)
    @property
    def get_scaleup_check(self):
        Qs = IcnReportDisaggregate.objects.filter(impact_id=self.impact_id).values('disaggregate__name').annotate(total_scaleup=Sum('actual_scaleup'), total_pilot=Sum('actual_pilot')).order_by('disaggregate__name')
        Qs2 = self.actual_impact_scaleup
        for q in Qs:
            if q['total_scaleup'] != Qs2:
                return False
            else:
                return True
    @property
    def get_pilot_check(self):
        Qs = IcnReportDisaggregate.objects.filter(impact_id=self.impact_id).values('disaggregate__name').annotate(total_scaleup=Sum('actual_scaleup'), total_pilot=Sum('actual_pilot')).order_by('disaggregate__name')
        Qs2 = self.actual_impact_pilot
        print(Qs2)
        for q in Qs:
            if q['total_pilot'] != Qs2:
                return False
            else:
                return True

    class Meta:
        ordering = ('id',)

class IcnReportDisaggregate(models.Model):
    icnreport =  models.ForeignKey(
        IcnReport, on_delete=models.CASCADE, null=True, blank=True)
    impact = models.ForeignKey(Impact, on_delete=models.CASCADE, null=True, blank=True)
    disaggregate = models.OneToOneField('conceptnote.Disaggregate', on_delete=models.CASCADE, null=True, blank=True)
   
    actual_pilot  = models.FloatField(null=True, blank=True)
    actual_scaleup  = models.FloatField(null=True, blank=True)   
    
    

    def __str__(self):
        return str(self.icnreport)


class ActivityReport(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    icnreport = models.ForeignKey(IcnReport, on_delete=models.DO_NOTHING, null=True, blank=True)
    actual_start_date = models.DateField()
    actual_end_date = models.DateField()
    aworeda = models.ManyToManyField(ImplementationArea,  blank=True, related_name='program_aworedas')
    alead_agency = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='arcns')
    alead_co_agency = models.ManyToManyField(Portfolio,  blank=True, related_name='arco_leads')
    actual_reporting_date = models.DateField(null=True, blank=True)
    program_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='arprogram_lead')
    technical_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='artechnical_lead')
    mel_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='armel_lead')
    finance_lead = models.ForeignKey(UserRoles, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='arfinance_lead')
    description = models.TextField(null=True, blank=True)
   
    
    actual_mc_budget = models.FloatField(null=True, blank=True)
    
    actual_cost_sharing_budget = models.FloatField(null=True, blank=True)
    USD = 1
    ETB = 2
    CURRENCY_CHOICES =   (
        (USD, '$'),
        (ETB, 'Br'),
     
        )

 
    mc_currency = models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES, default = 1, blank=True, null=True)
    cs_currency =  models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES, default = 1, blank=True, null=True)
   
    
   

    STATUS_CHOICES = [(False, 'Draft'), (True, 'Submitted')]
    status = models.BooleanField("Status", default=False, 
                                       choices=STATUS_CHOICES)
    approval_status = models.CharField(max_length=100,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_name(self):
        return "ActivityReport"
        
       
    def __str__(self):
        return self.activity.title

class ActivityReportImplementationArea(models.Model):
    activityreport =  models.ForeignKey(
        ActivityReport, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(
        NRegion, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(
        NZone, on_delete=models.CASCADE, null=True, blank=True)
    woreda = models.OneToOneField(NWoreda, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
    
class ActivityReportImpact(models.Model):
    activityreport =  models.ForeignKey(
        ActivityReport, on_delete=models.CASCADE, null=True, blank=True)
    activityimpact =  models.OneToOneField(
        ActivityImpact, on_delete=models.CASCADE, null=True, blank=True)
   
    
    actual_impact_pilot  = models.FloatField(null=True, blank=True)
    actual_impact_scaleup  = models.FloatField(null=True, blank=True)
    

    def __str__(self):
        return str(self.pk)

class ActivityReportDocument(models.Model):
    user = models.ForeignKey(User, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='activityreportuploaded_by')
    activityreport = models.ForeignKey(ActivityReport, on_delete=models.CASCADE,  blank=True)
    description = models.TextField(blank=True, null=True)
    document = models.FileField(null=True,  blank=True, max_length=500, upload_to=path_and_rename, validators=[FileExtensionValidator(allowed_extensions=["doc","docx","pdf" ])])
    ver = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,  null=True,  blank=True)

    class Meta:
        ordering = ('-uploaded_at',)
    
    def __str__(self):
        return "%s %s %s" % ("Version", self.ver, self.user.username)

class ActivityReportSubmit(models.Model):
  
    id = models.AutoField(primary_key=True)
    activityreport =  models.ForeignKey(
        ActivityReport, on_delete=models.CASCADE, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    submission_status = models.ForeignKey(Submission_Status, on_delete=models.CASCADE)
    submission_note = models.TextField(null=True,  blank=True)

    document = models.ForeignKey(ActivityReportDocument, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ('-submission_date',)
    
    
    def save(self, *args, **kwargs):
        if self.submission_date and self.old_submission_date != self.submission_date:
            self.submission_date = timezone.now()
        super(ActivityReportSubmit, self).save(*args, **kwargs)
   
    
    def __str__(self):
        return str(self.id)

class ActivityReportSubmitApproval_T(models.Model):
   
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(ActivityReportSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(ActivityReportDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(ActivityReportSubmitApproval_T, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(ActivityReportSubmitApproval_T, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)

class ActivityReportSubmitApproval_M(models.Model):
   
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(ActivityReportSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(ActivityReportDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(ActivityReportSubmitApproval_M, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(ActivityReportSubmitApproval_M, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)

class ActivityReportSubmitApproval_P(models.Model):
    Pending_Review = 1
    Require_Doc_Update = 2
    Approved = 3
    Rejected = 4
    STATUS = (
        (Pending_Review, 'Pending Review'),
        (Require_Doc_Update, 'Require Doc Update'),
        (Approved, 'Request Approved'),
        (Rejected, 'Request Rejected'),
        )

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(ActivityReportSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalf_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(ActivityReportDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(ActivityReportSubmitApproval_P, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(ActivityReportSubmitApproval_P, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)

class ActivityReportSubmitApproval_F(models.Model):
    Pending_Review = 1
    Require_Doc_Update = 2
    Approved = 3
    Rejected = 4
    STATUS = (
        (Pending_Review, 'Pending Review'),
        (Require_Doc_Update, 'Require Doc Update'),
        (Approved, 'Request Approved'),
        (Rejected, 'Request Rejected'),
        )

    
    user = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    submit_id = models.OneToOneField(ActivityReportSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalt_Status, on_delete=models.CASCADE)
    document = models.ForeignKey(ActivityReportDocument, on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs):
        super(ActivityReportSubmitApproval_F, self).__init__(*args, **kwargs)
        self.old_approval_status = self.approval_status
        self.old_document = self.document
        
    
    def save(self, *args, **kwargs):
        if (self.approval_status and self.old_approval_status != self.approval_status) or (self.document and self.old_document != self.document):
            self.approval_date = timezone.now()
        super(ActivityReportSubmitApproval_F, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.id)